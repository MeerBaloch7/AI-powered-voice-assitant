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

    def execute(self, command: str) -> bool:
        cmd = command.lower()
        seconds = 0

        match = re.search(r"(\d+)\s*(minute|minutes|min|mins)", cmd)
        if match:
            seconds += int(match.group(1)) * 60

        match = re.search(r"(\d+)\s*(second|seconds|sec|secs)", cmd)
        if match:
            seconds += int(match.group(1))

        if seconds > 0:
            threading.Timer(seconds, self._timer_finished, args=[seconds]).start()
            print(f"Timer set for {seconds} seconds.")
            return True

        return False

    def _timer_finished(self, total_seconds: int):
        minutes = total_seconds // 60
        secs = total_seconds % 60
        label = f"{minutes} minute(s)" if minutes else ""
        if secs:
            label = f"{label} {secs} second(s)" if label else f"{secs} second(s)"
        print(f"Timer finished! {label} has passed.")
