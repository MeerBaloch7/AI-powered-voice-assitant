import webbrowser
from .base_plugin import BasePlugin


class SearchGooglePlugin(BasePlugin):
    name = "Search Google"
    intent = "search_google"
    patterns = ["search google", "google search", "search for", "look up"]

    def execute(self, command: str) -> bool:
        # Extract the query part after the trigger phrase
        query = command.strip()
        if not query:
            return False

        address = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(address)
        return True
