import pytest
import os


FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


def test_fixture_wav_exists():
    path = os.path.join(FIXTURE_DIR, "test_audio.wav")
    assert os.path.exists(path), "test_audio.wav fixture not found"
    assert os.path.getsize(path) > 44, "WAV file too small (header only)"


def test_transcribe_returns_none_for_bad_audio():
    from SRM import SpeechRecognitionModule
    import speech_recognition as sr

    srm = SpeechRecognitionModule()
    with sr.AudioFile(os.path.join(FIXTURE_DIR, "test_audio.wav")) as source:
        audio = srm.recognizer.record(source)
    # Silence should produce empty or no transcription
    result = srm.transcribe(audio)
    assert result is None or result == ""


def test_recognize_speech_returns_none_without_microphone(mocker):
    from SRM import SpeechRecognitionModule
    mocker.patch.object(SpeechRecognitionModule, "capture_audio", return_value=None)
    srm = SpeechRecognitionModule()
    assert srm.recognize_speech() is None
