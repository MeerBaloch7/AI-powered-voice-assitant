import os
import struct
import threading
import time

from NLPM import NaturalLanguageProcessingModule
from CEM import CommandExecutionModule
from TTS import TextToSpeechModule
from SRM import SpeechRecognitionModule
from commands import plugins
from config import Config
from conversation_context import ConversationContext


class TriggerMode:
    WAKE = "wake"
    HOTKEY = "hotkey"
    BOTH = "both"


class SmartListener:
    def __init__(self, srm: SpeechRecognitionModule, nlpm: NaturalLanguageProcessingModule,
                 cem: CommandExecutionModule, tts: TextToSpeechModule,
                 config: Config, context: ConversationContext):
        self.srm = srm
        self.nlpm = nlpm
        self.cem = cem
        self.tts = tts
        self.config = config
        self.context = context
        self.trigger_mode = config.trigger.mode

        self._running = True
        self._wake_detected = threading.Event()
        self._hotkey_detected = threading.Event()
        self._wake_active = threading.Event()
        self._wake_active.set()

        self._porcupine = None
        self._pa = None
        self._wake_stream = None

    def stop(self):
        self._running = False
        self._wake_detected.set()
        self._hotkey_detected.set()
        self._wake_active.set()

    def run(self):
        if self.trigger_mode in (TriggerMode.WAKE, TriggerMode.BOTH):
            self._try_init_wake_word()

        if self.trigger_mode in (TriggerMode.HOTKEY, TriggerMode.BOTH):
            self._init_hotkey()

        if self.trigger_mode == TriggerMode.WAKE and self._porcupine is None:
            print("[Error] Wake word unavailable. No trigger available. Exiting.")
            return

        while self._running:
            self._wait_for_trigger()
            if not self._running:
                break

            self._wake_active.clear()
            self._process_voice_command()
            self._wake_active.set()

        self._cleanup()

    def _try_init_wake_word(self):
        try:
            import pvporcupine
            import pyaudio as pa_module

            access_key = self.config.picovoice_access_key
            if not access_key:
                print("[Warning] PICOVOICE_ACCESS_KEY not set. Wake word disabled.")
                if self.trigger_mode == TriggerMode.WAKE:
                    return
                print("[Info] Falling back to hotkey-only mode.")

            self._porcupine = pvporcupine.create(
                access_key=access_key,
                keywords=["hey assistant"],
            )
            self._pa = pa_module.PyAudio()
            self._wake_stream = self._pa.open(
                rate=self._porcupine.sample_rate,
                channels=1,
                format=pa_module.paInt16,
                input=True,
                frames_per_buffer=self._porcupine.frame_length,
            )

            thread = threading.Thread(target=self._wake_loop, daemon=True)
            thread.start()
            print("[Info] Wake word active — say 'Hey Assistant'")
        except ImportError:
            print("[Error] pvporcupine or pyaudio not installed.")
            if self.trigger_mode == TriggerMode.WAKE:
                raise
            print("[Info] Falling back to hotkey-only mode.")

    def _wake_loop(self):
        while self._running:
            self._wake_active.wait()
            if not self._running:
                break

            pcm = self._wake_stream.read(self._porcupine.frame_length, exception_on_overflow=False)
            pcm_array = struct.unpack_from("h" * self._porcupine.frame_length, pcm)
            result = self._porcupine.process(pcm_array)
            if result >= 0:
                keyword = self._porcupine.keywords[result] if hasattr(self._porcupine, "keywords") else "wake word"
                print(f"[Wake] {keyword}")
                self._wake_detected.set()

    def _init_hotkey(self):
        try:
            import keyboard
            hotkey = self.config.trigger.hotkey
            keyboard.add_hotkey(hotkey, self._on_hotkey, suppress=True)
            print(f"[Info] Hotkey active — press {hotkey} to start recording")
        except ImportError:
            print("[Error] keyboard module not installed.")
            if self.trigger_mode in (TriggerMode.HOTKEY, TriggerMode.BOTH):
                if self.trigger_mode == TriggerMode.HOTKEY:
                    raise

    def _on_hotkey(self):
        self._hotkey_detected.set()

    def _wait_for_trigger(self):
        while self._running:
            if self._hotkey_detected.is_set():
                self._hotkey_detected.clear()
                return
            if self._wake_detected.is_set():
                self._wake_detected.clear()
                return
            time.sleep(0.05)

    def _process_voice_command(self):
        audio = self.srm.capture_audio()
        if audio is None:
            print("[Error] Failed to capture audio from microphone.")
            return

        text = self.srm.transcribe(audio)
        if not text:
            print("[Info] No speech recognized.")
            return

        print(f"\n[Transcription] {text}")
        intent = self.nlpm.recognize_intent(text, self.context)
        success = self.cem.execute(intent, text, self.context)

        if success:
            plugin = plugins.get(intent)
            msg = f"{plugin.name}." if plugin else "Command executed successfully."
        else:
            msg = "I could not complete the command."

        if not self.tts.speak(msg):
            print(f"[Text Output] {msg}")

        print(f"[Result] intent={intent} success={success}")

    def _cleanup(self):
        if self._wake_stream:
            self._wake_stream.close()
        if self._pa:
            self._pa.terminate()
        if self._porcupine:
            self._porcupine.delete()
