import logging
from typing import Optional

from commands import plugins
from conversation_context import ConversationContext

logger = logging.getLogger(__name__)


class CommandExecutionModule:
    def execute(self, intent: str, command: str = "", context: Optional[ConversationContext] = None) -> bool:
        plugin = plugins.get(intent)
        if plugin is None:
            logger.warning("Unrecognized intent: %s", intent)
            return False

        plugin.context_data.clear()
        plugin.previous_data = context.last_data if context else {}
        try:
            success = plugin.execute(command)
        except Exception as e:
            logger.error("Plugin '%s' raised an exception: %s", intent, e)
            return False

        if context and success:
            context.add_turn(command, intent, success, plugin.context_data)

        return success
