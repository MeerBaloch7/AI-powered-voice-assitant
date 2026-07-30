import os
from .base_plugin import BasePlugin


class OpenNotepadPlugin(BasePlugin):
    name = "Open Notepad"
    intent = "open_notepad"
    patterns = ["open notepad", "start notepad"]

    def execute(self, command: str) -> bool:
        if os.name == "nt":
            os.system("start notepad")
            return True

        print("Open notepad is only supported on Windows in this implementation.")
        return False
