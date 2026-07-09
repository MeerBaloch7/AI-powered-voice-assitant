import pyttsx3
from typing import Optional


class TextToSpeechModule:
    """Offline text-to-speech module using pyttsx3."""

    def __init__(self, voice_name: Optional[str] = None, rate: Optional[int] = None, volume: Optional[float] = None):
        self.engine = pyttsx3.init()

        if voice_name:
            self._set_voice(voice_name)

        if rate is not None:
            self.engine.setProperty("rate", rate)

        if volume is not None:
            self.engine.setProperty("volume", max(0.0, min(1.0, volume)))

    def _set_voice(self, voice_name: str) -> None:
        voices = self.engine.getProperty("voices")
        for voice in voices:
            if voice_name.lower() in voice.name.lower():
                self.engine.setProperty("voice", voice.id)
                return

    def speak(self, text: str) -> bool:
        if not text or not text.strip():
            return False

        self.engine.say(text.strip())
        self.engine.runAndWait()
        return True


if __name__ == "__main__":
    tts = TextToSpeechModule()
    tts.speak("This is the Text-to-Speech module speaking.")
