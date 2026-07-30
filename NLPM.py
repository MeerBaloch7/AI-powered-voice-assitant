from typing import Literal

from commands import plugins

Intent = Literal[
    "open_notepad", "search_google", "open_calculator",
    "open_explorer", "volume_control", "screenshot",
    "lock_pc", "open_website", "get_weather",
    "set_timer", "create_note", "clipboard_actions",
    "unknown_command",
]


class NaturalLanguageProcessingModule:
    def recognize_intent(self, command: str) -> str:
        if not command or not command.strip():
            return "unknown_command"

        cmd = command.lower().strip()

        for intent, plugin in plugins.items():
            for pattern in plugin.patterns:
                if pattern in cmd:
                    return intent

        return "unknown_command"
