import logging
import os

from ._utils import launch_windows_app
from .base_plugin import BasePlugin

logger = logging.getLogger(__name__)


class OpenNotepadPlugin(BasePlugin):
    name = "Open Notepad"
    intent = "open_notepad"
    patterns = ["open notepad", "start notepad"]

    def execute(self, command: str) -> bool:
        if os.name == "nt":
            return launch_windows_app("notepad")

        logger.info("Open notepad is only supported on Windows in this implementation.")
        return False
