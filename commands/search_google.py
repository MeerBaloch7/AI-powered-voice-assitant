import logging
import webbrowser
from urllib.parse import quote_plus

from .base_plugin import BasePlugin

logger = logging.getLogger(__name__)


class SearchGooglePlugin(BasePlugin):
    name = "Search Google"
    intent = "search_google"
    patterns = ["search google", "google search", "search for", "look up"]

    def execute(self, command: str) -> bool:
        query = command.strip()
        if not query:
            return False

        lower = query.lower()
        for phrase in self.patterns:
            if lower.startswith(phrase):
                query = query[len(phrase):].strip()
                for connector in ("for ", "about ", "the "):
                    if query.lower().startswith(connector):
                        query = query[len(connector):].strip()
                        break
                break

        if not query:
            return False

        address = f"https://www.google.com/search?q={quote_plus(query)}"
        webbrowser.open(address)
        return True
