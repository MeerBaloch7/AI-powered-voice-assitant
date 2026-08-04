import os
import importlib
import inspect
import logging
from .base_plugin import BasePlugin

logger = logging.getLogger(__name__)

_COMMANDS_DIR = os.path.dirname(__file__)


def _discover_plugins() -> dict[str, BasePlugin]:
    discovered = {}
    for fname in sorted(os.listdir(_COMMANDS_DIR)):
        if fname.startswith("_") or not fname.endswith(".py"):
            continue
        module_name = fname[:-3]
        try:
            module = importlib.import_module(f".{module_name}", __package__)
        except Exception as e:
            logger.error("Failed to load plugin module %s: %s", module_name, e)
            continue
        for _, cls in inspect.getmembers(module, inspect.isclass):
            if issubclass(cls, BasePlugin) and cls is not BasePlugin:
                try:
                    instance = cls()
                except Exception as e:
                    logger.error("Failed to instantiate plugin %s: %s", cls.__name__, e)
                    continue
                if instance.intent in discovered:
                    logger.warning("Duplicate intent '%s' — %s overrides %s",
                                   instance.intent, type(instance).__name__, type(discovered[instance.intent]).__name__)
                discovered[instance.intent] = instance
    return discovered


plugins: dict[str, BasePlugin] = _discover_plugins()
