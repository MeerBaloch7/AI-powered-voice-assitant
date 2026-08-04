import logging

import speech_recognition as sr
import numpy as np

logger = logging.getLogger(__name__)


class SpeechRecognitionModule:
    def __init__(self, model_name: str = "base.en"):
        self.recognizer = sr.Recognizer()
        self._model = None
        self._model_name = model_name

    def _get_model(self):
        if self._model is None:
            import whisper
            self._model = whisper.load_model(self._model_name)
        return self._model

    def capture_audio(self):
        try:
            logger.info("Listening...")
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            return audio
        except OSError as e:
            logger.error("Microphone not found or not accessible: %s", e)
            return None
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            logger.info("No speech detected within the timeout.")
            return None

    def recognize_speech(self):
        audio = self.capture_audio()
        if audio is None:
            return None
        return self.transcribe(audio)

    def transcribe(self, audio):
        try:
            raw = audio.get_raw_data()
            audio_np = np.frombuffer(raw, dtype=np.int16)
            audio_np = audio_np.astype(np.float32) / 32768
            result = self._get_model().transcribe(audio_np, language='en', fp16=False)
            text = result['text'].strip()
            logger.info("Recognized text: %s", text)
            return text
        except Exception as e:
            logger.error("Whisper transcription failed: %s", e)
            return None


if __name__ == "__main__":
    srm = SpeechRecognitionModule()
    result = srm.recognize_speech()
    if result:
        print("\nFinal Text:", result)
    else:
        print("\nNo speech recognized.")
