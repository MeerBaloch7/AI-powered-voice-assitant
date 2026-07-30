import argparse
import threading

from SRM import SpeechRecognitionModule
from NLPM import NaturalLanguageProcessingModule
from CEM import CommandExecutionModule
from TTS import TextToSpeechModule
from GUI import GraphicalUserInterface
from smart_listener import SmartListener
from config import Config
from conversation_context import ConversationContext


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


def start_voice(config: Config, trigger_override: str | None = None):
    if not _check_microphone():
        print("[Error] No microphone detected. Voice input unavailable.")
        print("[Info] Use --mode gui for text-only interaction.")
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
    listener.run()


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
        thread = threading.Thread(target=start_voice, args=(config, trigger), daemon=True)
        thread.start()
        GraphicalUserInterface().run()
