import re
from typing import Literal

Intent = Literal["open_notepad", "search_google", "unknown_command"]

class NaturalLanguageProcessingModule:
    """
    Rule-based intent recognizer (Algorithm II).
    """

    OPEN_NOTEPAD_RE = re.compile(r"\b(open|start)\s+(notepad)\b", re.IGNORECASE)
    SEARCH_GOOGLE_RE = re.compile(r"\b(google\s+search|search)\b", re.IGNORECASE)

    def recognize_intent(self, command: str) -> Intent:
        if not command or not command.strip():
            return "unknown_command"

        cmd = command.lower().strip()

        if self.OPEN_NOTEPAD_RE.search(cmd):
            return "open_notepad"

        if self.SEARCH_GOOGLE_RE.search(cmd):
            return "search_google"

        return "unknown_command"

