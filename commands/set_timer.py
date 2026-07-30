import re
import threading
from .base_plugin import BasePlugin


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

    def execute(self, command: str) -> bool:
        cmd = command.lower()
        seconds = self._parse_duration(cmd)

        if seconds > 0:
            if self._active_timer:
                self._active_timer.cancel()
            self._active_timer = threading.Timer(seconds, self._timer_finished)
            self._active_timer.daemon = True
            self._active_timer.start()
            print(f"Timer set for {seconds} seconds.")
            self.context_data = {"duration": seconds}
            return True

        return False

    def _parse_duration(self, cmd: str) -> int:
        seconds = 0
        match = re.search(r"(\d+)\s*(minute|minutes|min|mins)", cmd)
        if match:
            seconds += int(match.group(1)) * 60
        match = re.search(r"(\d+)\s*(second|seconds|sec|secs)", cmd)
        if match:
            seconds += int(match.group(1))
        return seconds

    def _timer_finished(self):
        print("Timer finished!")
        self._active_timer = None
