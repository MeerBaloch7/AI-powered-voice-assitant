import logging
import os

from ._utils import launch_windows_app
from .base_plugin import BasePlugin

logger = logging.getLogger(__name__)


class LockPcPlugin(BasePlugin):
    name = "Lock PC"
    intent = "lock_pc"
    patterns = [
        "lock pc", "lock computer", "lock my computer",
        "lock my pc", "lock workstation", "lock screen",
    ]

    def execute(self, command: str) -> bool:
        if os.name == "nt":
            return launch_windows_app("rundll32.exe", "user32.dll,LockWorkStation")

        return False
