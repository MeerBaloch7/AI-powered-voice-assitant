import os
from .base_plugin import BasePlugin


class OpenCalculatorPlugin(BasePlugin):
    name = "Open Calculator"
    intent = "open_calculator"
    patterns = ["open calculator", "launch calculator", "start calculator", "open calc"]

    def execute(self, command: str) -> bool:
        if os.name == "nt":
            os.system("start calc")
            return True

        return False
