import sys
import threading
import time
import types
from unittest.mock import MagicMock

import pytest

from config import Config
from smart_listener import SmartListener


@pytest.fixture
def fake_keyboard(monkeypatch):
    mod = types.ModuleType("keyboard")
    mod.add_hotkey = MagicMock()
    monkeypatch.setitem(sys.modules, "keyboard", mod)
    return mod


@pytest.fixture
def fake_wake(monkeypatch):
    porcupine_mod = types.ModuleType("pvporcupine")
    porcupine_mod.create = MagicMock()
    pyaudio_mod = types.ModuleType("pyaudio")
    pyaudio_mod.PyAudio = MagicMock()
    pyaudio_mod.paInt16 = 8
    monkeypatch.setitem(sys.modules, "pvporcupine", porcupine_mod)
    monkeypatch.setitem(sys.modules, "pyaudio", pyaudio_mod)
    return porcupine_mod, pyaudio_mod


@pytest.fixture
def no_trigger_modules(monkeypatch):
    monkeypatch.setitem(sys.modules, "pvporcupine", None)
    monkeypatch.setitem(sys.modules, "pyaudio", None)
    monkeypatch.setitem(sys.modules, "keyboard", None)


@pytest.fixture
def listener_mocks():
    srm = MagicMock()
    srm.capture_audio.return_value = MagicMock()
    srm.transcribe.return_value = "open notepad"
    nlpm = MagicMock()
    nlpm.recognize_intent.return_value = "open_notepad"
    cem = MagicMock()
    cem.execute.return_value = True
    tts = MagicMock()
    tts.speak.return_value = True
    return srm, nlpm, cem, tts


def make_listener(srm, nlpm, cem, tts, mode="hotkey"):
    cfg = Config()
    cfg.trigger.mode = mode
    return SmartListener(srm, nlpm, cem, tts, config=cfg, context=None)


def test_hotkey_flow_processes_command_and_releases_wake_active(listener_mocks, fake_keyboard):
    srm, nlpm, cem, tts = listener_mocks
    processing = threading.Event()

    def hooked(*args, **kwargs):
        processing.set()
        return MagicMock()

    srm.capture_audio.side_effect = hooked
    listener = make_listener(srm, nlpm, cem, tts, mode="hotkey")

    thread = threading.Thread(target=listener.run)
    thread.start()
    try:
        listener._hotkey_detected.set()
        assert processing.wait(timeout=2), "command was not processed after hotkey trigger"
        time.sleep(0.1)
        assert listener._wake_active.is_set(), "wake active flag was not restored"
        assert cem.execute.called
    finally:
        listener.stop()
        thread.join(timeout=2)
    assert not thread.is_alive()


def test_processing_exception_does_not_kill_loop(listener_mocks, fake_keyboard):
    srm, nlpm, cem, tts = listener_mocks
    cem.execute.side_effect = RuntimeError("boom")
    listener = make_listener(srm, nlpm, cem, tts, mode="hotkey")

    thread = threading.Thread(target=listener.run)
    thread.start()
    try:
        listener._hotkey_detected.set()
        time.sleep(0.2)
        assert listener._wake_active.is_set(), "wake active flag was not restored after exception"
        assert thread.is_alive(), "listener thread died after plugin exception"
    finally:
        listener.stop()
        thread.join(timeout=2)
    assert not thread.is_alive()


def test_wake_mode_without_access_key_disables_wake_word(listener_mocks, fake_wake):
    porcupine_mod, _ = fake_wake
    srm, nlpm, cem, tts = listener_mocks
    listener = make_listener(srm, nlpm, cem, tts, mode="wake")

    listener.run()

    porcupine_mod.create.assert_not_called()
    assert listener._porcupine is None


def test_wake_init_failure_is_graceful(listener_mocks, fake_wake):
    porcupine_mod, _ = fake_wake
    porcupine_mod.create.side_effect = RuntimeError("invalid access key")
    srm, nlpm, cem, tts = listener_mocks
    listener = make_listener(srm, nlpm, cem, tts, mode="wake")

    listener.run()

    assert listener._porcupine is None


def test_no_trigger_available_exits_immediately(listener_mocks, no_trigger_modules):
    srm, nlpm, cem, tts = listener_mocks
    listener = make_listener(srm, nlpm, cem, tts, mode="both")

    start = time.time()
    listener.run()
    assert time.time() - start < 1.0


def test_stale_triggers_cleared_before_processing(listener_mocks, fake_keyboard):
    srm, nlpm, cem, tts = listener_mocks
    listener = make_listener(srm, nlpm, cem, tts, mode="hotkey")
    listener._wake_detected.set()
    listener._hotkey_detected.set()

    listener._process_voice_command()

    assert not listener._wake_detected.is_set()
    assert not listener._hotkey_detected.is_set()


def test_stop_releases_blocked_thread(listener_mocks, fake_keyboard):
    srm, nlpm, cem, tts = listener_mocks
    listener = make_listener(srm, nlpm, cem, tts, mode="hotkey")

    thread = threading.Thread(target=listener.run)
    thread.start()
    time.sleep(0.1)
    listener.stop()
    thread.join(timeout=2)
    assert not thread.is_alive()
