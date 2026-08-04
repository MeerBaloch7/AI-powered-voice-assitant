import logging
import os
from datetime import datetime
from .base_plugin import BasePlugin

logger = logging.getLogger(__name__)


class ScreenshotPlugin(BasePlugin):
    name = "Take Screenshot"
    intent = "screenshot"
    patterns = [
        "take screenshot", "screenshot", "capture screen",
        "take a screenshot", "screen capture",
    ]

    def execute(self, command: str) -> bool:
        try:
            import pyautogui

            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            path = os.path.join(desktop, f"screenshot_{timestamp}.png")

            screenshot = pyautogui.screenshot()
            screenshot.save(path)
            logger.info("Screenshot saved to: %s", path)
            return True
        except ImportError:
            logger.error("pyautogui is not installed. Run: pip install pyautogui pillow")
            return False
        except Exception as e:
            logger.error("Screenshot failed: %s", e)
            return False
