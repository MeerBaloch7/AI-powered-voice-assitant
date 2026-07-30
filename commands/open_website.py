import webbrowser
from .base_plugin import BasePlugin

_WEBSITES = {
    "youtube": "https://www.youtube.com",
    "reddit": "https://www.reddit.com",
    "github": "https://www.github.com",
    "stack overflow": "https://stackoverflow.com",
    "gmail": "https://mail.google.com",
    "google": "https://www.google.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://www.twitter.com",
    "linkedin": "https://www.linkedin.com",
    "amazon": "https://www.amazon.com",
    "netflix": "https://www.netflix.com",
}


class OpenWebsitePlugin(BasePlugin):
    name = "Open Website"
    intent = "open_website"
    patterns = [
        "open youtube", "open reddit", "open github",
        "open gmail", "open google", "open facebook",
        "open twitter", "open linkedin", "open amazon",
        "open netflix", "open stack overflow",
        "go to youtube", "go to github",
    ]

    def execute(self, command: str) -> bool:
        cmd = command.lower()
        for name, url in _WEBSITES.items():
            if name in cmd:
                webbrowser.open(url)
                print(f"Opening {name}")
                return True

        return False
