import re
from .base_plugin import BasePlugin


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
            print("Volume control is only supported on Windows in this implementation.")
            return False

        import pycaw.pycaw
        from pycaw.api.endpoint import AudioEndpoint

        if "mute" in cmd:
            self._set_mute(True)
            return True
        if "unmute" in cmd:
            self._set_mute(False)
            return True

        match = re.search(r"(\d+)", cmd)
        if match:
            target = int(match.group(1))
            self._set_volume(target / 100.0)
        elif "up" in cmd or "increase" in cmd:
            self._change_volume(+0.1)
        elif "down" in cmd or "decrease" in cmd:
            self._change_volume(-0.1)

        return True

    def _set_volume(self, level: float):
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(max(0.0, min(1.0, level)), None)

    def _change_volume(self, delta: float):
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current = volume.GetMasterVolumeLevelScalar()
        self._set_volume(current + delta)

    def _set_mute(self, muted: bool):
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(int(muted), None)


import os
