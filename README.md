# jotts
JoTTS is a German text-to-speech engine using tacotron and griffin-lim. The synthesizer model
has been trained on my voice. Due to real time usage I decided not to include a vocoder and use
griffin-lim instead which results in a more robotic voice but is much faster.

## Example usage

```python
jotts = JoTTS()
jotts.speak("Das Wetter heute ist fabulös.", True)
jotts.text2wav("Es war aber auch schon einmal besser!")
```

## Disclaimer
I hope that my vote will be used only for legal and ethical purposes. Please do not get into mischief with it.
