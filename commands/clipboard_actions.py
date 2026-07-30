from .base_plugin import BasePlugin


class ClipboardActionsPlugin(BasePlugin):
    name = "Clipboard Actions"
    intent = "clipboard_actions"
    patterns = [
        "what is on my clipboard", "what's on my clipboard",
        "read clipboard", "show clipboard", "clipboard content",
        "copy to clipboard", "paste from clipboard",
    ]

    def execute(self, command: str) -> bool:
        try:
            import pyperclip

            cmd = command.lower()

            if "read" in cmd or "show" in cmd or "what" in cmd:
                content = pyperclip.paste()
                if content:
                    print(f"Clipboard content: {content}")
                else:
                    print("Clipboard is empty.")
                return True

            return False
        except ImportError:
            print("pyperclip is not installed. Run: pip install pyperclip")
            return False
