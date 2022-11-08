import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from jotts import JoTTS

if __name__ == "__main__":
	tts = JoTTS()
	tts.list_models()
	tts.load_models(force_model_download=False, model_name="jonas_v0.1")
	#tts.speak("Das ist ein Test mit meiner Stimme.", wait_for_end = True, use_wavernn_vocoder=True)
	#tts.speak("Das ist ein Test mit meiner Stimme.", wait_for_end = True, use_wavernn_vocoder=False)
	tts.textToWav(text="Das ist ein Test mit meiner Stimme.", out_path="vocoder_out.wav", use_wavernn_vocoder=True)
	tts.textToWav(text="Das ist ein Test mit meiner Stimme.", out_path="griffin_lim_out.wav", use_wavernn_vocoder=False)