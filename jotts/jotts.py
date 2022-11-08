from .synthesizer.inference import Synthesizer
from .vocoder import inference as vocoder
from pathlib import Path
import numpy as np
import soundfile as sf
import librosa
import torch
import sys
import os
import sounddevice as sd
import time
from loguru import logger
import json
import urllib.request
from tqdm import tqdm

class DownloadProgressBar(tqdm):
	def update_to(self, b=1, bsize=1, tsize=None):
		if tsize is not None:
			self.total = tsize
		self.update(b * bsize - self.n)

class JoTTS:

	def __init__(self):
		self.VOCODER_RELEASE = "vocoder_v0.1"
		self.SYNTHESIZER_DOWNLOAD_URL = "https://github.com/padmalcom/jotts/releases/download/{release}/{file}.pt"
		self.VOCODER_DOWNLOAD_URL = "https://github.com/padmalcom/jotts/releases/download/{vocoder_release}/{vocoder_file}.pt".format(vocoder_release=self.VOCODER_RELEASE, vocoder_file=self.VOCODER_RELEASE)
		
	def __get_released_models__(self):
		page = 1
		releases = {}
		while True:
			with urllib.request.urlopen(f"https://api.github.com/repos/padmalcom/jotts/releases?per_page=100&page={page}") as response:
				data = response.read()
				encoding = response.info().get_content_charset('utf-8')
				json_data = json.loads(data.decode(encoding))
				for d in json_data:
					if not d.get('tag_name').startswith("vocoder"):
						releases[d.get('tag_name')] = d.get('assets')[0].get('browser_download_url')
				if not json_data:
					break
				page += 1
		return releases
		
	def list_models(self):
		models = self.__get_released_models__()
		for m in models:
			print("Model name:", m, "model url:", models[m])
		
	def __prepare_model__(self, model_name, force_model_download):
		synthesizer_url = self.SYNTHESIZER_DOWNLOAD_URL.format(release=model_name, file=model_name)
		model_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "saved_models")
		
		if not os.path.exists(model_path):
			os.makedirs(model_path)
		
		synthesizer_model_path = os.path.join(model_path, "{model_name}.pt".format(model_name=model_name))
		vocoder_model_path = os.path.join(model_path, "{model_name}.pt".format(model_name=self.VOCODER_RELEASE))
		
		# Is there no or a newer model?
		if not os.path.exists(synthesizer_model_path) or force_model_download == True:
			if not os.path.exists(synthesizer_model_path):
				logger.debug("There is no synthesizer or vocoder model yet, downloading...")
			else:
				if force_model_download:
					if os.path.exists(synthesizer_model_path):
						os.remove(synthesizer_model_path)
					logger.debug("Forced download starting...")
				else:
					logger.debug("There is a newer model, downloading...")
				
			# Downloading the latest tts model release
			logger.debug("Download synthesizer model: {}", syn_url)
			with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=syn_url.split('/')[-1]) as t:
				urllib.request.urlretrieve(syn_url, filename=synthesizer_model_path, reporthook=t.update_to)
				
		if not os.path.exists(vocoder_model_path) or force_model_download:
			logger.debug("Download vocoder model: {}", self.VOCODER_DOWNLOAD_URL)
			with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=self.VOCODER_DOWNLOAD_URL.split('/')[-1]) as t:
				urllib.request.urlretrieve(self.VOCODER_DOWNLOAD_URL, filename=vocoder_model_path, reporthook=t.update_to)
		else:
			logger.info("No need to download vocoder {}.", self.VOCODER_RELEASE)
				
		return synthesizer_model_path, vocoder_model_path

	def load_models(self, model_name = "jonas_v0.1", force_model_download=False):
		models = self.__get_released_models__()
		if not model_name in models:
			logger.error("The model {} does not exists. Use list_models() to see which models exist.", model_name)
			return
		
		logger.debug("Loading model {}...", model_name)
		
		synthesizer_model_path, vocoder_model_path = self.__prepare_model__(model_name, force_model_download)
			
		if torch.cuda.is_available():
			device_id = torch.cuda.current_device()
			gpu_properties = torch.cuda.get_device_properties(device_id)
			logger.debug("Found %d GPUs available. Using GPU %d (%s) of compute capability %d.%d with "
			"%.1fGb total memory.\n" % 
			(torch.cuda.device_count(),
			device_id,
			gpu_properties.name,
			gpu_properties.major,
			gpu_properties.minor,
			gpu_properties.total_memory / 1e9))
		else:
			logger.debug("Using CPU for inference.")
			
		logger.debug("Loading the synthesizer...")
		self.synthesizer = Synthesizer(Path(synthesizer_model_path))
		vocoder.load_model(Path(vocoder_model_path))

	def _replace_umlauts(self, string):
		u = 'ü'.encode()
		U = 'Ü'.encode()
		a = 'ä'.encode()
		A = 'Ä'.encode()
		o = 'ö'.encode()
		O = 'Ö'.encode()
		ss = 'ß'.encode()

		string = string.encode()
		string = string.replace(u, b'ue')
		string = string.replace(U, b'Ue')
		string = string.replace(a, b'ae')
		string = string.replace(A, b'Ae')
		string = string.replace(o, b'oe')
		string = string.replace(O, b'Oe')
		string = string.replace(ss, b'ss')

		string = string.decode('utf-8')
		return string

	def _gen_wav(self, text, use_wavernn_vocoder):
		text = self._replace_umlauts(text)
		texts = [text]
		embeds = [[0] * 256]
		specs = self.synthesizer.synthesize_spectrograms(texts, embeds)
		spec = specs[0]
		if use_wavernn_vocoder:
			return vocoder.infer_waveform(spec)
		return Synthesizer.griffin_lim(spec)

	
	def speak(self, text, wait_for_end = False, use_wavernn_vocoder=False):
		generated_wav = self._gen_wav(text, use_wavernn_vocoder)
		audio_length = librosa.get_duration(generated_wav, sr = 14545)
		sd.play(generated_wav.astype(np.float32), round(self.synthesizer.sample_rate / 1.0))
		if wait_for_end:
			time.sleep(audio_length)

	def textToWav(self, text, out_path, use_wavernn_vocoder=False):
		generated_wav = self._gen_wav(text, use_wavernn_vocoder)
		sf.write(out_path, generated_wav.astype(np.float32), round(self.synthesizer.sample_rate / 1.0))