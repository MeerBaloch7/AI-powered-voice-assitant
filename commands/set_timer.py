import logging
import re
import threading
from .base_plugin import BasePlugin

logger = logging.getLogger(__name__)


class SetTimerPlugin(BasePlugin):
    name = "Set Timer"
    intent = "set_timer"
    patterns = [
        "set timer", "set a timer", "start timer",
        "timer for", "remind me in", "countdown",
    ]
    follow_up_patterns = [
        "make that", "make it", "change that to", "change to",
        "set to", "update to", "actually",
    ]

    _active_timer: threading.Timer | None = None
    _next_token: int = 0
    _lock = threading.Lock()

    def execute(self, command: str) -> bool:
        cmd = command.lower()
        seconds = self._parse_duration(cmd)

        if seconds == 0:
            match = re.search(r"(\d+)", cmd)
            prev_seconds = self.previous_data.get("duration")
            if not match or not prev_seconds:
                return False
            unit = self.previous_data.get("unit", "minutes")
            seconds = int(match.group(1)) * (60 if unit == "minutes" else 1)

        with self._lock:
            if self._active_timer is not None:
                self._active_timer.cancel()
            token = self._next_token
            self._next_token += 1
            timer = threading.Timer(seconds, self._timer_finished, args=[token])
            timer.daemon = True
            timer.start()
            self._active_timer = timer

        logger.info("Timer set for %s seconds.", seconds)
        self.context_data = {"duration": seconds, "unit": "minutes" if seconds % 60 == 0 and seconds >= 60 else "seconds"}
        return True

    def _parse_duration(self, cmd: str) -> int:
        seconds = 0
        match = re.search(r"(\d+)\s*(minute|minutes|min|mins)", cmd)
        if match:
            seconds += int(match.group(1)) * 60
        match = re.search(r"(\d+)\s*(second|seconds|sec|secs)", cmd)
        if match:
            seconds += int(match.group(1))
        return seconds

    def _timer_finished(self, token: int):
        logger.info("Timer finished!")
        with self._lock:
            if self._active_timer is not None and self._next_token - 1 == token:
                self._active_timer = None
