# AI Powered Voice Assistant

A modular, plugin-based voice assistant built in Python. Supports speech recognition via Whisper, rule-based intent classification, offline text-to-speech, and a Tkinter GUI — all orchestrated through an extensible plugin architecture.

---

# Table of Contents

1. [Speech Recognition Module (SRM)](#1-speech-recognition-module-srm)
2. [Natural Language Processing Module (NLPM)](#2-natural-language-processing-module-nlpm)
3. [Plugin Architecture](#3-plugin-architecture)
4. [Command Execution Module (CEM)](#4-command-execution-module-cem)
5. [Available Commands](#5-available-commands)
6. [Text-to-Speech Module (TTS)](#6-text-to-speech-module-tts)
7. [Graphical User Interface Module (GUI)](#7-graphical-user-interface-module-gui)
8. [System Integration and Execution](#8-system-integration-and-execution)
9. [Installation](#9-installation)
10. [Usage](#10-usage)
11. [Plugin Development Guide](#11-plugin-development-guide)

---

# 1. Speech Recognition Module (SRM)

A Python-based Speech-to-Text (STT) module that captures microphone audio using `SpeechRecognition` and transcribes it with OpenAI's Whisper `base.en` model. Raw audio is converted to NumPy arrays for Whisper processing.

**Pipeline:**

```
User Speaks
     |
     v
Initialize Recognizer
     |
     v
Adjust for Ambient Noise
     |
     v
Capture Audio Input
     |
     v
Convert to NumPy Array
     |
     v
Whisper Transcript
     |
     v
Return Text
```

**Key features:**
- Offline transcription using Whisper `base.en`
- Ambient noise adjustment before capture
- Fallback handling for microphone errors

---

# 2. Natural Language Processing Module (NLPM)

The NLPM determines the user's intent from the transcribed text.

**Algorithm: Plugin-Matched Intent Recognition**
- Input: A user-issued command (string).
- Output: A semantic label classifying the command's inferred purpose.

Steps:
1. Begin
2. Convert the command to lowercase.
3. Iterate over all registered plugins.
4. For each plugin, check if any of its `patterns` appear in the command.
5. If a match is found, return that plugin's `intent`.
6. If no plugin matches, return `"unknown_command"`.
7. End

**Key features:**
- No hardcoded regex — patterns come from plugins in `commands/`.
- Adding a new intent means creating a new plugin file; NLPM discovers it automatically.
- Simple substring matching (case-insensitive).

---

# 3. Plugin Architecture

Commands are organized as self-contained plugins in the `commands/` folder. Each plugin is a Python file that defines a class inheriting from `BasePlugin`.

**Plugin interface:**

| Property / Method | Type | Description |
|-------------------|------|-------------|
| `name`           | `str` | Human-readable label (e.g. "Open Calculator") |
| `intent`         | `str` | Machine identifier (e.g. "open_calculator") |
| `patterns`       | `list[str]` | Trigger phrases for NLPM matching |
| `execute(command)` | `bool` | Run the command action |

**Auto-discovery:** On import, `commands/__init__.py` scans the directory, loads every `.py` file, finds `BasePlugin` subclasses, and registers them in a `plugins` dict keyed by `intent`.

**Adding a new plugin:** Drop a new `.py` file into `commands/` with a class inheriting `BasePlugin`. No changes to NLPM, CEM, or any other file.

---

# 4. Command Execution Module (CEM)

The CEM receives an intent and command string, then dispatches execution to the matching plugin.

**Algorithm: Plugin Dispatch Execution**
- Input:
  - `intent`: A string representing the recognized intent.
  - `command`: The original user command string.
- Output: The corresponding plugin executes, or a failure is returned.

Steps:
1. Begin
2. Look up `intent` in the `plugins` registry.
3. If found, call `plugin.execute(command)` and return the result.
4. If not found, print an error and return `False`.
5. End

**Key features:**
- No if/elif chains — dispatch is fully dynamic.
- Every plugin receives the full command text for context-aware processing.

---

# 5. Available Commands

| Intent | Trigger Phrases | Action |
|--------|----------------|--------|
| `open_notepad` | "open notepad", "start notepad" | Opens Notepad (Windows) |
| `search_google` | "search google", "google search", "search for", "look up" | Opens browser with Google search |
| `open_calculator` | "open calculator", "launch calculator", "start calculator", "open calc" | Opens Calculator (Windows) |
| `open_explorer` | "open explorer", "open file explorer", "open file manager", "show my files", "open my computer", "open this pc" | Opens File Explorer (Windows) |
| `volume_control` | "volume up", "volume down", "set volume", "increase volume", "decrease volume", "mute", "unmute", "turn up volume", "turn down volume" | Adjusts system volume (Windows, requires `pycaw`) |
| `screenshot` | "take screenshot", "screenshot", "capture screen", "take a screenshot", "screen capture" | Saves screenshot to desktop (requires `pyautogui`) |
| `lock_pc` | "lock pc", "lock computer", "lock my computer", "lock my pc", "lock workstation", "lock screen" | Locks workstation (Windows) |
| `open_website` | "open youtube", "open reddit", "open github", "open gmail", "open google", "go to youtube", etc. | Opens supported websites in browser |
| `get_weather` | "weather", "what is the weather", "weather today", "weather report", "temperature", "forecast" | Fetches weather from wttr.in (requires `requests`) |
| `set_timer` | "set timer", "set a timer", "start timer", "timer for", "remind me in", "countdown" | Sets a countdown timer (supports minutes/seconds) |
| `create_note` | "create note", "make a note", "write note", "take note", "new note", "save note", "reminder", "note down" | Saves a `.txt` note to desktop |
| `clipboard_actions` | "what is on my clipboard", "what's on my clipboard", "read clipboard", "show clipboard", "clipboard content", "copy to clipboard" | Reads clipboard content (requires `pyperclip`) |

---

# 6. Text-to-Speech Module (TTS)

Offline speech synthesis using `pyttsx3`.

**Algorithm: Text-to-Speech Generation**
- Input: A string text representing the verbal response to be synthesized.
- Output: Audible spoken output through the system's speech engine.

Steps:
1. Begin
2. Initialize the offline speech synthesis engine.
3. Pass the response text to the TTS engine.
4. Activate speech output.
5. End

**Key features:**
- Fully offline — no internet required.
- Configurable voice, rate, and volume.

---

# 7. Graphical User Interface Module (GUI)

A Tkinter-based GUI for users who prefer typing over speaking.

**Algorithm: GUI Execution Workflow**
- Input: User-provided text command via GUI input field.
- Output: The corresponding action is executed, and a response dialog is displayed.

Steps:
1. Begin
2. Initialize the main application window.
3. Set window title to "Speech Assistant GUI".
4. Create a text input field for commands.
5. Add an "Execute" button that triggers `on_submit()`.
6. `on_submit()`:
   a. Retrieve the text from the input field.
   b. Forward the text to NLPM for intent recognition.
   c. Send the intent and full command to CEM for execution.
   d. Display a dialog with the recognized plugin name and result.
7. Start the Tkinter event loop.
8. End

**Key features:**
- Tkinter-based for cross-platform compatibility.
- Displays the resolved plugin name for confirmation.

---

# 8. System Integration and Execution

All modules are combined in `main.py` to enable seamless interaction between voice, text, and GUI interfaces.

**Algorithm: Integrated Voice Assistant Workflow**
- Objective: Enable uninterrupted monitoring of user speech, identify intent, execute the relevant operation, and deliver audible feedback while preserving GUI responsiveness.

Steps:
1. Begin
2. Initialize and display the GUI in the main thread.
3. Start a parallel thread dedicated to voice interactions.
4. Inside the voice thread, loop continuously:
   a. Capture speech via the SRM.
   b. If valid speech is detected:
      i. Forward the transcribed command to NLPM for intent recognition.
      ii. Send the intent and command to CEM for plugin dispatch.
      iii. Activate TTS for audible feedback using the plugin name.
5. Ensure both GUI and voice threads run concurrently.
6. End

**Key features:**
- Multithreaded — voice loop runs in a daemon thread, GUI stays responsive.
- Three modes: `voice`, `gui`, or `integrated` (default, runs both).

---

# 9. Installation

### Prerequisites

- Python 3.10 or higher
- A working microphone
- `ffmpeg` installed and available in PATH (required by Whisper)

### Steps

```bash
# 1. Create a virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt
```

### Dependencies

| Package | Required For |
|---------|-------------|
| `SpeechRecognition` | Audio capture |
| `PyAudio` | Microphone access |
| `openai-whisper` | Speech-to-text transcription |
| `numpy` | Audio data conversion |
| `pyttsx3` | Offline text-to-speech |
| `pyautogui` | Screenshot capture |
| `pyperclip` | Clipboard read/write |
| `pillow` | Image handling (screenshot) |
| `requests` | Weather API calls |
| `pycaw` | Volume control (Windows) |

---

# 10. Usage

```bash
# Voice-only mode (microphone required)
python main.py --mode voice

# GUI-only mode (type commands)
python main.py --mode gui

# Integrated mode (GUI + voice thread, default)
python main.py

# Via the launcher script
python run.py
python run.py --mode voice
```

### Example Commands

| Say or type | Result |
|------------|--------|
| "Open Notepad" | Opens Notepad |
| "Search Google for Python" | Opens Google search |
| "Open calculator" | Opens Calculator |
| "Take screenshot" | Saves screenshot to desktop |
| "Lock my computer" | Locks the workstation |
| "Open YouTube" | Opens YouTube in browser |
| "What's the weather in London" | Shows weather for London |
| "Set timer for 5 minutes" | Starts a 5-minute countdown |
| "Create note buy groceries" | Saves note to desktop |
| "What's on my clipboard" | Reads clipboard content |
| "Turn up the volume" | Increases system volume |

---

# 11. Plugin Development Guide

### Creating a New Plugin

1. Create a new `.py` file in the `commands/` folder.
2. Import and inherit `BasePlugin`.
3. Define `name`, `intent`, `patterns`, and `execute()`.
4. Restart the application — the plugin is auto-discovered.

**Example — `commands/open_chrome.py`:**

```python
import os
from .base_plugin import BasePlugin

class OpenChromePlugin(BasePlugin):
    name = "Open Chrome"
    intent = "open_chrome"
    patterns = ["open chrome", "launch chrome", "start chrome"]

    def execute(self, command: str) -> bool:
        if os.name == "nt":
            os.system("start chrome")
            return True
        return False
```

### Plugin Guidelines

- Keep patterns specific enough to avoid false matches.
- Use `os.name` checks for cross-platform support.
- Handle `ImportError` gracefully if a plugin depends on an optional library.
- Return `True` on success, `False` on failure.

---

# Project Structure

```
AI-powered-voice-assistant/
├── commands/                  # Plugin directory
│   ├── __init__.py            # Auto-discovery engine
│   ├── base_plugin.py         # Abstract base class
│   ├── open_notepad.py
│   ├── search_google.py
│   ├── open_calculator.py
│   ├── open_explorer.py
│   ├── volume_control.py
│   ├── screenshot.py
│   ├── lock_pc.py
│   ├── open_website.py
│   ├── get_weather.py
│   ├── set_timer.py
│   ├── create_note.py
│   └── clipboard_actions.py
├── SRM.py                     # Speech Recognition Module
├── NLPM.py                    # Natural Language Processing Module
├── CEM.py                     # Command Execution Module
├── TTS.py                     # Text-to-Speech Module
├── GUI.py                     # Graphical User Interface
├── main.py                    # Entry point
├── run.py                     # CLI launcher
├── requirements.txt
├── AGENTS.md
└── README.md
```
