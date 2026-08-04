import logging
import os
import re

from .base_plugin import BasePlugin

logger = logging.getLogger(__name__)


class VolumeControlPlugin(BasePlugin):
    name = "Volume Control"
    intent = "volume_control"
    patterns = [
        "volume up", "volume down", "set volume",
        "increase volume", "decrease volume",
        "mute", "unmute", "turn up volume", "turn down volume",
    ]

    def execute(self, command: str) -> bool:
        cmd = command.lower()

        if os.name != "nt":
            logger.info("Volume control is only supported on Windows in this implementation.")
            return False

        try:
            if "unmute" in cmd:
                self._set_mute(False)
                return True
            if "mute" in cmd:
                self._set_mute(True)
                return True

            match = re.search(r"(\d+)", cmd)
            if match:
                target = int(match.group(1))
                self._set_volume(target / 100.0)
            elif "up" in cmd or "increase" in cmd:
                self._change_volume(+0.1)
            elif "down" in cmd or "decrease" in cmd:
                self._change_volume(-0.1)
        except Exception as e:
            logger.error("Volume control failed: %s", e)
            return False

        return True

    def _get_volume_interface(self):
        from pycaw.pycaw import AudioUtilities
        device = AudioUtilities.GetSpeakers()
        return device.EndpointVolume

    def _set_volume(self, level: float):
        volume = self._get_volume_interface()
        volume.SetMasterVolumeLevelScalar(max(0.0, min(1.0, level)), None)

    def _change_volume(self, delta: float):
        volume = self._get_volume_interface()
        current = volume.GetMasterVolumeLevelScalar()
        self._set_volume(current + delta)

    def _set_mute(self, muted: bool):
        volume = self._get_volume_interface()
        volume.SetMute(int(muted), None)
