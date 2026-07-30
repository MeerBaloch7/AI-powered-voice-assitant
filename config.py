import json, os
from dataclasses import dataclass, field

@dataclass
class TriggerConfig:
    mode: str = "both"
    hotkey: str = "ctrl+shift+v"

@dataclass
class TTSConfig:
    voice: str | None = None
    rate: int | None = 200
    volume: float | None = 1.0

@dataclass
class Config:
    picovoice_access_key: str = ""
    trigger: TriggerConfig = field(default_factory=TriggerConfig)
    tts: TTSConfig = field(default_factory=TTSConfig)

    @classmethod
    def load(cls, path="config.json"):
        cfg = cls()
        if os.path.exists(path):
            with open(path) as f:
                data = json.load(f)
            if "picovoice_access_key" in data:
                cfg.picovoice_access_key = data["picovoice_access_key"]
            if "trigger" in data:
                cfg.trigger = TriggerConfig(**data["trigger"])
            if "tts" in data:
                cfg.tts = TTSConfig(**data["tts"])
        cfg.picovoice_access_key = os.environ.get("PICOVOICE_ACCESS_KEY", cfg.picovoice_access_key)
        return cfg