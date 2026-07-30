from typing import Optional

from commands import plugins
from conversation_context import ConversationContext


class CommandExecutionModule:
    def execute(self, intent: str, command: str = "", context: Optional[ConversationContext] = None) -> bool:
        plugin = plugins.get(intent)
        if plugin is None:
            print(f"Unrecognized intent: {intent}")
            return False

        plugin.context_data.clear()
        success = plugin.execute(command)

        if context and success:
            context.add_turn(command, intent, success, plugin.context_data)

        return success
