import pytest
import os


FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


def test_fixture_wav_exists():
    path = os.path.join(FIXTURE_DIR, "test_audio.wav")
    assert os.path.exists(path), "test_audio.wav fixture not found"
    assert os.path.getsize(path) > 44, "WAV file too small (header only)"


def test_model_not_loaded_at_construction(mocker):
    from SRM import SpeechRecognitionModule
    get_model = mocker.patch.object(SpeechRecognitionModule, "_get_model")
    SpeechRecognitionModule()
    get_model.assert_not_called()


def test_transcribe_returns_none_for_bad_audio(mocker):
    from SRM import SpeechRecognitionModule
    import speech_recognition as sr

    fake_model = mocker.Mock()
    fake_model.transcribe.return_value = {"text": ""}
    mocker.patch.object(SpeechRecognitionModule, "_get_model", return_value=fake_model)

    srm = SpeechRecognitionModule()
    with sr.AudioFile(os.path.join(FIXTURE_DIR, "test_audio.wav")) as source:
        audio = srm.recognizer.record(source)
    result = srm.transcribe(audio)
    assert result is None or result == ""


def test_transcribe_returns_none_on_whisper_error(mocker):
    from SRM import SpeechRecognitionModule

    fake_model = mocker.Mock()
    fake_model.transcribe.side_effect = RuntimeError("model exploded")
    mocker.patch.object(SpeechRecognitionModule, "_get_model", return_value=fake_model)

    srm = SpeechRecognitionModule()
    audio = mocker.Mock()
    audio.get_raw_data.return_value = b"\x00\x00" * 16000
    assert srm.transcribe(audio) is None


def test_recognize_speech_returns_none_without_microphone(mocker):
    from SRM import SpeechRecognitionModule
    mocker.patch.object(SpeechRecognitionModule, "capture_audio", return_value=None)
    srm = SpeechRecognitionModule()
    assert srm.recognize_speech() is None
