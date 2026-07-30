import os
import importlib
import inspect
from .base_plugin import BasePlugin

_COMMANDS_DIR = os.path.dirname(__file__)


def _discover_plugins() -> dict[str, BasePlugin]:
    discovered = {}
    for fname in os.listdir(_COMMANDS_DIR):
        if fname.startswith("_") or not fname.endswith(".py"):
            continue
        module_name = fname[:-3]
        module = importlib.import_module(f".{module_name}", __package__)
        for _, cls in inspect.getmembers(module, inspect.isclass):
            if issubclass(cls, BasePlugin) and cls is not BasePlugin:
                instance = cls()
                discovered[instance.intent] = instance
    return discovered


plugins: dict[str, BasePlugin] = _discover_plugins()
