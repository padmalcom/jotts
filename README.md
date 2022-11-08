# jotts
JoTTS is a German text-to-speech engine using tacotron and griffin-lim or wavernn as vocoder. The synthesizer model
has been trained on my voice using tacotron1. Using grifin-lim as vocoder makes the audio generation much faster
whereas using a trained vocoder returns better results in most cases.

<a href="https://www.buymeacoffee.com/padmalcom" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>


## API
- First create an instance of *JoTTS*.

- (optional) List all models that are available *using list_models()*. You can also look them up in the browser: https://github.com/padmalcom/Real-Time-Voice-Cloning-German/releases

- Load a model of your choice using *load_models()* which takes *force_model_download* as an optional parameter
in case that the last download of the synthesizer failed and the model cannot be applied. The parameter
*model_name* is validated against all available models on the release page.

- Call speak with a *text* parameter that contains the text to speak out loud. The second parameter *wait_for_end*
can be set to True, to wait until speaking is done, e.g. to prevent your application to close. If you want
to use a trained vocoder, set *use_wavernn_vocoder* to True.

- Use *textToWav* to create a wav file instead of speaking the text. *out_path* specifies where the wav file is
written to. Use *use_wavernn_vocoder* to use a trained vocoder.

## Example usage

```python
from jotts import JoTTS
if __name__ == "__main__":
	tts = JoTTS()
	tts.list_models()
	tts.load_models(force_model_download=False, model_name="jonas_v0.1")
	tts.speak("Das ist ein Test mit meiner Stimme.", wait_for_end = True, use_wavernn_vocoder=True)
	tts.speak("Das ist ein Test mit meiner Stimme.", wait_for_end = True, use_wavernn_vocoder=False)
	tts.textToWav(text="Das ist ein Test mit meiner Stimme.", out_path="vocoder_out.wav", use_wavernn_vocoder=True)
	tts.textToWav(text="Das ist ein Test mit meiner Stimme.", out_path="griffin_lim_out.wav", use_wavernn_vocoder=False)
```

## Todo
- Add an option to change the default audio device to speak the text
- Add threading or multi processing to allow speaking without blocking
- Add a parameter to avoid online communication in case of running JoTTS on edge.
- Add a feature to quickly finetune a model with a arbitrary voice

## Training a model for your own voice
Training a synthesizer model is easy - if you know how to do it. I created a course on udemy to show you how it is done.
Don't buy the tutorial for the full price, there is a discout every month :-) 

https://www.udemy.com/course/voice-cloning/

If you neither have the backgroud or the resources or if you are just lazy or too rich, contact me for contract work.
Cloning a voice normally needs ~15 Minutes of clean audio from the voice you want to clone.

## Disclaimer
I hope that my (and any other person's) voice will be used only for legal and ethical purposes. Please do not get into mischief with it.
