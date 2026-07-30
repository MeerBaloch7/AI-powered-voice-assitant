from commands import plugins


class CommandExecutionModule:
    def execute(self, intent: str, command: str = "") -> bool:
        plugin = plugins.get(intent)
        if plugin is not None:
            return plugin.execute(command)

        print(f"Unrecognized intent: {intent}")
        return False
