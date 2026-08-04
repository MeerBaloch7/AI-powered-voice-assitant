from typing import Optional

from commands import plugins
from conversation_context import ConversationContext


class NaturalLanguageProcessingModule:
    def recognize_intent(self, command: str, context: Optional[ConversationContext] = None) -> str:
        if not command or not command.strip():
            return "unknown_command"

        cmd = command.lower().strip()

        # First pass: direct plugin patterns, longest match wins so resolution
        # does not depend on filesystem discovery order.
        best_intent = None
        best_length = -1
        for intent, plugin in plugins.items():
            for pattern in plugin.patterns:
                if pattern in cmd and len(pattern) > best_length:
                    best_intent = intent
                    best_length = len(pattern)

        if best_intent is not None:
            return best_intent

        # Second pass: context follow-up. If the last command succeeded and the
        # plugin that handled it declares follow-up patterns, match them.
        if context is not None and context.last_turn and context.last_turn.success:
            last_intent = context.last_intent
            plugin = plugins.get(last_intent)
            if plugin is not None:
                for pattern in plugin.follow_up_patterns:
                    if pattern in cmd:
                        return last_intent

        return "unknown_command"
