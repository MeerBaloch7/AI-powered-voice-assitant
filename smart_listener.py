import logging
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

logger = logging.getLogger(__name__)


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
        self._wake_thread = None
        self._hotkey_available = False

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

        if self._porcupine is None and not self._hotkey_available:
            logger.error("No trigger available (wake word and hotkey both failed). Exiting.")
            return

        try:
            while self._running:
                self._wait_for_trigger()
                if not self._running:
                    break

                self._wake_active.clear()
                try:
                    self._process_voice_command()
                except Exception as e:
                    logger.error("Voice command processing failed: %s", e)
                finally:
                    self._wake_active.set()
        finally:
            self._cleanup()

    def _try_init_wake_word(self):
        try:
            import pvporcupine
            import pyaudio as pa_module
        except ImportError:
            logger.error("pvporcupine or pyaudio not installed. Wake word disabled.")
            return

        access_key = self.config.picovoice_access_key
        if not access_key:
            logger.warning("PICOVOICE_ACCESS_KEY not set. Wake word disabled.")
            return

        try:
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

            self._wake_thread = threading.Thread(target=self._wake_loop, daemon=True)
            self._wake_thread.start()
            logger.info("Wake word active — say 'Hey Assistant'")
        except Exception as e:
            logger.error("Failed to initialize wake word: %s", e)
            self._wake_stream = None
            self._porcupine = None
            if self._pa:
                self._pa.terminate()
                self._pa = None

    def _wake_loop(self):
        frame_length = self._porcupine.frame_length
        fmt = "h" * frame_length
        while self._running:
            self._wake_active.wait()
            if not self._running:
                break

            try:
                pcm = self._wake_stream.read(frame_length, exception_on_overflow=False)
                if not self._wake_active.is_set():
                    continue
                pcm_array = struct.unpack_from(fmt, pcm)
                result = self._porcupine.process(pcm_array)
                if result >= 0:
                    keyword = self._porcupine.keywords[result] if hasattr(self._porcupine, "keywords") else "wake word"
                    logger.info("[Wake] %s", keyword)
                    self._wake_detected.set()
            except Exception as e:
                if not self._running:
                    break
                logger.error("Wake word loop error: %s", e)
                time.sleep(0.1)

    def _init_hotkey(self):
        try:
            import keyboard
            hotkey = self.config.trigger.hotkey
            keyboard.add_hotkey(hotkey, self._on_hotkey, suppress=True)
            self._hotkey_available = True
            logger.info("Hotkey active — press %s to start recording", hotkey)
        except ImportError:
            logger.error("keyboard module not installed. Hotkey disabled.")
        except Exception as e:
            logger.error("Failed to register hotkey: %s", e)

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
        self._wake_detected.clear()
        self._hotkey_detected.clear()

        audio = self.srm.capture_audio()
        if audio is None:
            logger.error("Failed to capture audio from microphone.")
            return

        text = self.srm.transcribe(audio)
        if not text:
            logger.info("No speech recognized.")
            return

        logger.info("[Transcription] %s", text)
        intent = self.nlpm.recognize_intent(text, self.context)
        success = self.cem.execute(intent, text, self.context)

        if success:
            plugin = plugins.get(intent)
            msg = f"{plugin.name}." if plugin else "Command executed successfully."
        else:
            msg = "I could not complete the command."

        if not self.tts.speak(msg):
            logger.info("[Text Output] %s", msg)

        logger.info("[Result] intent=%s success=%s", intent, success)

    def _cleanup(self):
        try:
            if self._wake_stream:
                self._wake_stream.close()
        except Exception:
            pass
        self._wake_stream = None
        if self._pa:
            try:
                self._pa.terminate()
            except Exception:
                pass
            self._pa = None
        if self._porcupine:
            try:
                self._porcupine.delete()
            except Exception:
                pass
            self._porcupine = None
