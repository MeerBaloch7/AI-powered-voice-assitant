import logging
from typing import Optional

logger = logging.getLogger(__name__)


class TextToSpeechModule:
    """Offline text-to-speech module using pyttsx3."""

    def __init__(self, voice_name: Optional[str] = None, rate: Optional[int] = None, volume: Optional[float] = None):
        self.engine = None
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
        except Exception as e:
            logger.error("Could not initialize TTS engine: %s", e)
            return

        if voice_name:
            self._set_voice(voice_name)

        if rate is not None:
            self.engine.setProperty("rate", rate)

        if volume is not None:
            self.engine.setProperty("volume", max(0.0, min(1.0, volume)))

    def _set_voice(self, voice_name: str) -> None:
        if self.engine is None:
            return
        voices = self.engine.getProperty("voices")
        for voice in voices:
            if voice_name.lower() in voice.name.lower():
                self.engine.setProperty("voice", voice.id)
                return

    def speak(self, text: str) -> bool:
        if self.engine is None or not text or not text.strip():
            return False

        try:
            self.engine.say(text.strip())
            self.engine.runAndWait()
            return True
        except Exception as e:
            logger.error("Could not speak: %s", e)
            logger.info("[Text Output] %s", text.strip())
            return False

    def stop(self) -> None:
        if self.engine is None:
            return
        try:
            self.engine.stop()
        except Exception:
            pass


if __name__ == "__main__":
    tts = TextToSpeechModule()
    tts.speak("This is the Text-to-Speech module speaking.")
