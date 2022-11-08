from jotts import JoTTS

if __name__ == "__main__":
	tts = JoTTS()
	tts.list_models()
	tts.load_model(force_model_download=False, model_name="jonas_v0.1")
	#tts.speak("Das ist ein Test mit meiner Stimme.", True)