import logging
import os
from datetime import datetime
from .base_plugin import BasePlugin

logger = logging.getLogger(__name__)


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

        content = command.strip()
        lower = content.lower()
        for phrase in self.patterns:
            if lower.startswith(phrase):
                content = content[len(phrase):].strip()
                break
        if not content:
            content = command.strip()

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("Note saved to: %s", path)
            return True
        except OSError as e:
            logger.error("Failed to save note: %s", e)
            return False
