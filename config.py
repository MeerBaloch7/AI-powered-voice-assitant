import json
import logging
import os
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

VALID_TRIGGER_MODES = ("wake", "hotkey", "both")


def _coerce(value, cast, default, lo=None, hi=None):
    try:
        v = cast(value)
        if lo is not None:
            v = max(lo, v)
        if hi is not None:
            v = min(hi, v)
        return v
    except (TypeError, ValueError):
        return default


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
        data = {}
        if os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                logger.error("Could not read %s: %s", path, e)

        if not isinstance(data, dict):
            logger.error("%s must contain a JSON object.", path)
            data = {}

        if "picovoice_access_key" in data:
            cfg.picovoice_access_key = str(data["picovoice_access_key"])

        if isinstance(data.get("trigger"), dict):
            cfg.trigger = TriggerConfig(**{
                k: v for k, v in data["trigger"].items() if k in ("mode", "hotkey")
            })

        if isinstance(data.get("tts"), dict):
            tts_data = {k: v for k, v in data["tts"].items() if k in ("voice", "rate", "volume")}
            cfg.tts = TTSConfig(
                voice=tts_data.get("voice", cfg.tts.voice),
                rate=_coerce(tts_data.get("rate"), int, 200, -100, 500) if "rate" in tts_data else cfg.tts.rate,
                volume=_coerce(tts_data.get("volume"), float, 1.0, 0.0, 1.0) if "volume" in tts_data else cfg.tts.volume,
            )

        if cfg.trigger.mode not in VALID_TRIGGER_MODES:
            logger.error("Invalid trigger mode '%s'. Using 'both'.", cfg.trigger.mode)
            cfg.trigger.mode = "both"

        cfg.picovoice_access_key = os.environ.get("PICOVOICE_ACCESS_KEY", cfg.picovoice_access_key)
        return cfg
