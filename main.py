import argparse
import logging
import threading

from NLPM import NaturalLanguageProcessingModule
from CEM import CommandExecutionModule
from GUI import GraphicalUserInterface
from config import Config
from conversation_context import ConversationContext

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="Run the integrated speech assistant.")
    parser.add_argument(
        "--mode",
        choices=["voice", "gui", "integrated"],
        default="integrated",
        help="Select application mode: voice, gui, or integrated.",
    )
    parser.add_argument(
        "--trigger",
        choices=["wake", "hotkey", "both"],
        default=None,
        help="Override the config file trigger mode.",
    )
    return parser.parse_args()


def _check_microphone() -> bool:
    try:
        import speech_recognition as sr
        with sr.Microphone():
            return True
    except Exception:
        return False


def start_voice(config: Config, trigger_override: str | None = None, state: dict | None = None):
    from SRM import SpeechRecognitionModule
    from TTS import TextToSpeechModule
    from smart_listener import SmartListener

    if not _check_microphone():
        logger.error("No microphone detected. Voice input unavailable.")
        logger.info("Use --mode gui for text-only interaction.")
        return

    srm = SpeechRecognitionModule()
    nlpm = NaturalLanguageProcessingModule()
    cem = CommandExecutionModule()
    tts_config = config.tts
    tts = TextToSpeechModule(voice_name=tts_config.voice, rate=tts_config.rate, volume=tts_config.volume)
    context = ConversationContext()

    if trigger_override:
        config.trigger.mode = trigger_override

    listener = SmartListener(srm, nlpm, cem, tts, config=config, context=context)
    if state is not None:
        state["listener"] = listener
        state["tts"] = tts

    try:
        listener.run()
    finally:
        tts.stop()


if __name__ == "__main__":
    args = parse_args()
    config = Config.load()
    mode = args.mode
    trigger = args.trigger

    if mode == "gui":
        GraphicalUserInterface().run()
    elif mode == "voice":
        start_voice(config, trigger)
    else:
        voice_state: dict = {}

        def stop_voice():
            listener = voice_state.get("listener")
            if listener is not None:
                listener.stop()

        thread = threading.Thread(target=start_voice, args=(config, trigger, voice_state), daemon=True)
        thread.start()
        GraphicalUserInterface(on_close=stop_voice).run()
