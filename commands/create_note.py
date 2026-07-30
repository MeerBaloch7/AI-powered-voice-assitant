import os
from datetime import datetime
from .base_plugin import BasePlugin


class CreateNotePlugin(BasePlugin):
    name = "Create Note"
    intent = "create_note"
    patterns = [
        "create note", "make a note", "write note",
        "take note", "new note", "save note",
        "reminder", "note down",
    ]

    def execute(self, command: str) -> bool:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = os.path.join(desktop, f"note_{timestamp}.txt")

        content = command

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Note saved to: {path}")
            return True
        except OSError as e:
            print(f"Failed to save note: {e}")
            return False
