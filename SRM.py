import speech_recognition as sr
import whisper
import numpy as np


class SpeechRecognitionModule:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.model = whisper.load_model('base.en')

    def capture_audio(self):
        try:
            print("Listening...")
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            return audio
        except OSError as e:
            print(f"Error: microphone not found or not accessible. {e}")
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
            result = self.model.transcribe(audio_np, language='en', fp16=False)
            text = result['text'].strip()
            print("recognized text:", text)
            return text
        except Exception as e:
            print("whisper error", e)
            return None

    TranscribeAudio = transcribe


if __name__ == "__main__":
    srm = SpeechRecognitionModule()
    result = srm.recognize_speech()
    if result:
        print("\nFinal Text:", result)
    else:
        print("\nNo speech recognized.")
