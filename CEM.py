import os
import webbrowser
from typing import Optional


class CommandExecutionModule:
    def execute(self, intent: str, query: Optional[str] = None) -> bool:
        if intent == "open_notepad":
            return self._open_notepad()

        if intent == "search_google":
            return self._search_google(query)

        print(f"Unrecognized intent: {intent}")
        return False

    def _open_notepad(self) -> bool:
        if os.name == "nt":
            os.system("start notepad")
            return True

        print("Open notepad is only supported on Windows in this implementation.")
        return False

    def _search_google(self, query: Optional[str]) -> bool:
        if not query or not query.strip():
            print("No query provided for Google search.")
            return False

        address = f"https://www.google.com/search?q={query.strip().replace(' ', '+')}"
        webbrowser.open(address)
        return True