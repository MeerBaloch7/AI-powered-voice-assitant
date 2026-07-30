import os
import json
import pytest

from config import Config


def test_config_loads_defaults_when_file_missing(tmp_path):
    path = tmp_path / "nonexistent.json"
    cfg = Config.load(str(path))
    assert cfg.trigger.mode == "both"
    assert cfg.trigger.hotkey == "ctrl+shift+v"
    assert cfg.tts.rate == 200
    assert cfg.tts.volume == 1.0
    assert cfg.picovoice_access_key == ""


def test_config_loads_from_file(tmp_path):
    data = {
        "picovoice_access_key": "abc123",
        "trigger": {"mode": "hotkey", "hotkey": "ctrl+space"},
        "tts": {"voice": "zira", "rate": 150, "volume": 0.8},
    }
    path = tmp_path / "config.json"
    with open(path, "w") as f:
        json.dump(data, f)

    cfg = Config.load(str(path))
    assert cfg.picovoice_access_key == "abc123"
    assert cfg.trigger.mode == "hotkey"
    assert cfg.trigger.hotkey == "ctrl+space"
    assert cfg.tts.voice == "zira"
    assert cfg.tts.rate == 150
    assert cfg.tts.volume == 0.8


def test_env_var_overrides_file(tmp_path):
    data = {"picovoice_access_key": "from_file"}
    path = tmp_path / "config.json"
    with open(path, "w") as f:
        json.dump(data, f)

    os.environ["PICOVOICE_ACCESS_KEY"] = "from_env"
    try:
        cfg = Config.load(str(path))
        assert cfg.picovoice_access_key == "from_env"
    finally:
        del os.environ["PICOVOICE_ACCESS_KEY"]


def test_partial_config_keeps_defaults(tmp_path):
    data = {"trigger": {"mode": "wake"}}
    path = tmp_path / "config.json"
    with open(path, "w") as f:
        json.dump(data, f)

    cfg = Config.load(str(path))
    assert cfg.trigger.mode == "wake"
    assert cfg.trigger.hotkey == "ctrl+shift+v"
    assert cfg.tts.rate == 200
