import logging
import os

from ._utils import launch_windows_app
from .base_plugin import BasePlugin

logger = logging.getLogger(__name__)


class OpenExplorerPlugin(BasePlugin):
    name = "Open File Explorer"
    intent = "open_explorer"
    patterns = [
        "open explorer", "open file explorer",
        "open file manager", "show my files",
        "open my computer", "open this pc",
    ]

    def execute(self, command: str) -> bool:
        if os.name == "nt":
            return launch_windows_app("explorer")

        return False
