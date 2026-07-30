import os
from .base_plugin import BasePlugin


class LockPcPlugin(BasePlugin):
    name = "Lock PC"
    intent = "lock_pc"
    patterns = [
        "lock pc", "lock computer", "lock my computer",
        "lock my pc", "lock workstation", "lock screen",
    ]

    def execute(self, command: str) -> bool:
        if os.name == "nt":
            os.system("rundll32.exe user32.dll,LockWorkStation")
            return True

        return False
