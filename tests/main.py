from jotts import JoTTS

if __name__ == "__main__":
	tts = JoTTS(force_model_download=False)
	tts.speak("Das ist ein Test mit meiner Stimme.", True)