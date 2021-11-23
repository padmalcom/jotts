from .synthesizer.inference import Synthesizer
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

from github import Github
import urllib.request
from tqdm import tqdm

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

class JoTTS:

	# Not implemented yet, due to github rate limits
	#def __get_download_path__(self):
		# Identify latest release on github
		#g = Github()
		#repo = g.get_repo("padmalcom/jotts")
		#latest_release = repo.get_latest_release()		
		#DOWNLOAD_URL = latest_release.get_assets()[0].browser_download_url
		#MODEL_SIZE = latest_release.get_assets()[0].size
		#logger.debug("Latest model is {}.", DOWNLOAD_URL)
		#return DOWNLOAD_URL
		
	def __prepare_model__(self, force_model_download):
		DOWNLOAD_URL = "https://github.com/padmalcom/jotts/releases/download/v0.1/v0.1.pt"
		MODEL_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "saved_models")
		
		if not os.path.exists(MODEL_FILE):
			os.makedirs(MODEL_FILE)
			
		model_folder_empty = len(os.listdir(MODEL_FILE)) == 0
		
		MODEL_FILE = os.path.join(MODEL_FILE, "v0.1.pt")
		
		# Is there no or a newer model?
		if not os.path.exists(MODEL_FILE) or force_model_download == True:
			if model_folder_empty == True:
				logger.debug("There is no tts model yet, downloading...")
			else:
				if force_model_download:
					if os.path.exists(MODEL_FILE):
						os.remove(MODEL_FILE)
					logger.debug("Forced download starting...")
				else:
					logger.debug("There is a newer model, downloading...")
				
			# Downloading the latest tts model release
			logger.debug("Download file: {}", DOWNLOAD_URL)
			with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=DOWNLOAD_URL.split('/')[-1]) as t:
				urllib.request.urlretrieve(DOWNLOAD_URL, filename=MODEL_FILE, reporthook=t.update_to)
		return MODEL_FILE
		
	def __init__(self, force_model_download=False):
		logger.debug("Initializing JoTTS...")
		
		MODEL_FILE = self.__prepare_model__(force_model_download);
			
		self.syn_model_fpath = Path(MODEL_FILE)
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
		self.synthesizer = Synthesizer(self.syn_model_fpath)	
		
	def _gen_wav(self, text):
		texts = [text]
		embeds = [[0] * 256]
		specs = self.synthesizer.synthesize_spectrograms(texts, embeds)
		spec = specs[0]	 	
		return Synthesizer.griffin_lim(spec)

	
	def speak(self, text, do_sleep = False):
		generated_wav = self._gen_wav(text)
		audio_length = librosa.get_duration(generated_wav, sr = 14545)
		sd.play(generated_wav.astype(np.float32), round(self.synthesizer.sample_rate / 1.0))
		if do_sleep:
			time.sleep(audio_length)

	def textToWav(self, text, out_path='gen.wav'):
		generated_wav = self._gen_wav(text)
		sf.write(out_path, generated_wav.astype(np.float32), round(self.synthesizer.sample_rate / 1.0))