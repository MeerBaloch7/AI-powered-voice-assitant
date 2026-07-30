# AGENTS — AI assistant instructions for this repo

Purpose
- Short guidance for coding agents (Copilot-style) to be immediately productive in this workspace.

Quick facts
- **Python:** 3.10+
- **Main entry:** `main.py` — entry point with `--mode` and `--trigger` arguments.
- **Plugin system:** `commands/` folder — each file is a self-contained plugin auto-discovered at import.
- **Smart listening:** `smart_listener.py` — state machine with wake word (Porcupine) and/or push-to-talk hotkey (Ctrl+Shift+V).
- **Config:** `config.json` loaded by `config.py` — `Config` dataclass with env var overrides.
- **Conversation context:** `conversation_context.py` — stores recent turns for follow-up intent resolution.

How to run (local, interactive)
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py                          # integrated mode (GUI + voice)
python main.py --mode voice             # voice-only
python main.py --mode gui               # GUI-only
python main.py --trigger hotkey         # use push-to-talk instead of wake word
```

Modules overview
- `SRM.py` — `SpeechRecognitionModule`: captures mic audio with `SpeechRecognition`, transcribes with Whisper `base.en`.
- `NLPM.py` — `NaturalLanguageProcessingModule`: iterates plugin patterns to match intent; two-pass with context follow-up.
- `CEM.py` — `CommandExecutionModule`: dispatches intent to the matching plugin; reads `plugin.context_data` to update conversation history.
- `TTS.py` — `TextToSpeechModule`: offline speech synthesis via `pyttsx3`; configurable voice/rate/volume.
- `GUI.py` — `GraphicalUserInterface`: Tkinter window for text command input.
- `smart_listener.py` — `SmartListener`: IDLE → RECORDING → PROCESSING state machine; supports wake word + hotkey.
- `config.py` — `Config.load()` reads `config.json` + `PICOVOICE_ACCESS_KEY` env var.
- `conversation_context.py` — `ConversationContext`: stores last 5 turns; plugins can store arbitrary data per turn.
- `commands/` — plugin directory; each file inherits `BasePlugin` with `name`, `intent`, `patterns`, `execute()`.

Important implementation notes
- **Wake word** requires `PICOVOICE_ACCESS_KEY` env var (free at https://console.picovoice.ai/), set in `config.json` or env.
- **Hotkey** (Ctrl+Shift+V) works without any API key; configurable via config.json.
- `keyboard` and `pvporcupine` are optional imports — missing them falls back gracefully.
- Porcupine reads mic frames in a separate thread; its audio stream pauses during RECORDING state to avoid conflict with SRM's microphone access.
- `SRM.py` has two methods: `capture_audio()` returns raw audio, `transcribe(audio)` returns text.
- `BasePlugin` subclasses can override `follow_up_patterns` for context-aware follow-up commands.
- After `plugin.execute()`, CEM reads `plugin.context_data` dict and stores it in `ConversationContext`.

Testing guidance
- Unit-test logic that doesn't require live audio (plugin loading, intent matching, `smart_listener` state transitions, config loading, context management).
- For audio input, add small sample WAV files and tests that use `Recognizer.record()` on files instead of `Microphone`.
- Mock `pvporcupine` and `keyboard` in tests to avoid hardware dependency.

Contacts / Context
- README contains detailed installation steps and architectural notes: [README.md](README.md).

Revision history
- Updated to reflect plugin architecture, smart listening, config, and conversation context.
