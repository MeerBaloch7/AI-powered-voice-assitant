import argparse
import threading
import time

from SRM import SpeechRecognitionModule
from NLPM import NaturalLanguageProcessingModule
from CEM import CommandExecutionModule
from TTS import TextToSpeechModule
from GUI import GraphicalUserInterface


def process_command(command: str, nlpm: NaturalLanguageProcessingModule, cem: CommandExecutionModule, tts: TextToSpeechModule):
    intent = nlpm.recognize_intent(command)
    query = command if intent == "search_google" else None
    success = cem.execute(intent, query)

    if success:
        if intent == "open_notepad":
            tts.speak("Opening Notepad.")
        elif intent == "search_google":
            tts.speak(f"Searching Google for {command}.")
        else:
            tts.speak("Command executed successfully.")
    else:
        tts.speak("I could not complete the command.")

    return intent, success


def voice_loop():
    srm = SpeechRecognitionModule()
    nlpm = NaturalLanguageProcessingModule()
    cem = CommandExecutionModule()
    tts = TextToSpeechModule()

    while True:
        try:
            result = srm.recognize_speech()
            if result:
                print("\nFinal Text:", result)
                intent, success = process_command(result, nlpm, cem, tts)
                print(f"Detected intent: {intent} | Success: {success}")
            else:
                print("No speech recognized. Listening again...")
        except Exception as exc:
            print("Voice loop error:", exc)
        time.sleep(0.5)


def parse_args():
    parser = argparse.ArgumentParser(description="Run the integrated speech assistant.")
    parser.add_argument(
        "--mode",
        choices=["voice", "gui", "integrated"],
        default="integrated",
        help="Select application mode: voice, gui, or integrated.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    mode = args.mode

    if mode == "gui":
        GraphicalUserInterface().run()
    elif mode == "voice":
        voice_loop()
    else:
        thread = threading.Thread(target=voice_loop, daemon=True)
        thread.start()
        GraphicalUserInterface().run()
