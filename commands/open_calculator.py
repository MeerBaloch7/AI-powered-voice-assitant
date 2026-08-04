import logging
import os

from ._utils import launch_windows_app
from .base_plugin import BasePlugin

logger = logging.getLogger(__name__)


class OpenCalculatorPlugin(BasePlugin):
    name = "Open Calculator"
    intent = "open_calculator"
    patterns = ["open calculator", "launch calculator", "start calculator", "open calc"]

    def execute(self, command: str) -> bool:
        if os.name == "nt":
            return launch_windows_app("calc")

        return False
