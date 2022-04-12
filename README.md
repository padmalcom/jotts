# jotts
JoTTS is a German text-to-speech engine using tacotron and griffin-lim. The synthesizer model
has been trained on my voice using Tacotron1. Due to real time usage I decided not to include a vocoder and use
griffin-lim instead which results in a more robotic voice but is much faster.

<a href="https://www.buymeacoffee.com/padmalcom" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>


## API
- First create an instance of JoTTS. The initializer takes force_model_download as an optional parameter
in case that the last download of the synthesizer failed and the model cannot be applied.

- Call speak with a *text* parameter that contains the text to speak out loud. The second parameter
can be set to True, to wait until speaking is done.

- Use *textToWav* to create a wav file instead of speaking the text. 

## Example usage

```python
from jotts import JoTTS
jotts = JoTTS()
jotts.speak("Das Wetter heute ist fantastisch.", True)
jotts.textToWav("Es war aber auch schon mal besser!")
```

## Todo
- Add an option to change the default audio device to speak the text
- Add a parameter to select other models but the default model
- Add threading or multi processing to allow speaking without blocking
- Add a vocoder instead of griffin-lim to improve audio output.

## Training a model for your own voice
Training a synthesizer model is easy - if you know how to do it. I created a course on udemy to show you how it is done.
Don't buy the tutorial for the full price, there is a discout every month :-) 

https://www.udemy.com/course/voice-cloning/

If you neither have the backgroud or the resources or if you are just lazy or too rich, contact me for contract work.
Cloning a voice normally needs ~15 Minutes of clean audio from the voice you want to clone.

## Disclaimer
I hope that my (and any other person's) voice will be used only for legal and ethical purposes. Please do not get into mischief with it.
