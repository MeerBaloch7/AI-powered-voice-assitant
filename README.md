# AI voice assistant


# 1. Speech Recognition Module

A Python-based Speech-to-Text (STT) conversion module that leverages local audio capture and Whisper transcription for reliable speech recognition.

## Overview

This module captures microphone audio using `SpeechRecognition` and transcribes it with OpenAI's Whisper `base.en` model. The implementation converts raw audio data into NumPy arrays, then uses Whisper to produce text output without relying on Google Cloud or CMU Sphinx.

## Prerequisites

Before installing this module, ensure you have:
- Python 3.10 or higher
- A working microphone connected to your system
- `ffmpeg` installed on your system (required by Whisper)
- Audio libraries installed on your system (varies by OS)

## Installation

### Step 1: Create a Virtual Environment

```bash
python -m venv venv
On Windows: venv\Scripts\activate
```

### Step 2: Install Required Dependencies

```bash
pip install SpeechRecognition
pip install PyAudio
pip install numpy
pip install openai-whisper
pip install pyttsx3
```

## Architecture & Workflow

The module implements the following recognition pipeline:

```
           User Speaks
                 │
                 ▼
        Initialize Recognizer
                 │
                 ▼
       Adjust for Ambient Noise
                 │
                 ▼
          Capture Audio Input
                 │
                 ▼
        Convert to NumPy Array
                 │
                 ▼
         Whisper Transcript
                 │
                 ▼
             Return Text
```

---
# 2. Natural Language Processing Module (NLPM)

The Natural Language Processing Module (NLPM) processes the transcribed text and determines the intent behind the user‘s command.

**Algorithm II: Rule-Based Intent Recognition**
-  Input: A user-issued command (string).
- Output: A semantic label classifying the command's inferred purpose.

Steps:
1. Begin
2. Convert the command to lowercase.
3. If the command matches the regular expression for "open notepad" or "start notepad", then intent ← "open_notepad".
4. Else if the command matches the regular expression for "search" or "google search", then intent ← "search_google".
5. Else intent ← "unknown_command".
6. Return intent.
7. End

Key features:
- Uses regular expressions for pattern-based intent recognition.
- Recognizes multiple variations of a command (e.g., "open notepad", "start notepad").
- Simple, deterministic fallback to `unknown_command` when no pattern matches.

Example usages:
- "Open Notepad" → `open_notepad`
- "google search for python tutorials" → `search_google`
 

# 3. Command Execution Module (CEM)

The Command Execution Module (CEM) maps the detected intent to a corresponding system action.

**Algorithm III: Command Execution Algorithm**
- Input:
  - `intent`: A string representing the recognized intent.
  - `query` (optional): A string parameter required for search-type actions.
- Output: System executes the corresponding command or returns a failure notification.

Steps:
1. Begin
2. Switch based on the value of `intent`:
   a. Case `open_notepad`:
      i. Command the operating system to open the native text editor.
      ii. Break.
   b. Case `search_google`:
      i. If `query` is not empty:
         - Formulate a search address from the user query.
         - Launch the default browser to perform the search.
      ii. Else:
         - Display a message indicating that no query was provided.
      iii. Break.
   c. Default:
      i. Display an error indicating the command is unrecognized.
3. End

Key features:
- Executes system commands using `os.system()` for local actions.
- Opens URLs dynamically based on user queries using the web browser.
- Uses an optional `query` parameter for `search_google`.

# 4. Text-to-Speech Module (TTS)

The Text-to-Speech (TTS) Module generates verbal responses using `pyttsx3` for offline support.

**Algorithm IV: Text-to-Speech (TTS) Generation**
- Input: A string text representing the verbal response to be synthesized.
- Output: Audible spoken output rendered through the system's speech engine.

Steps:
1. Begin
   a. Initialize the offline speech synthesis engine.
   b. Forward the synthesized response text to the TTS system, where it is temporarily stored for speech conversion.
   c. Activate the text-to-speech engine to transform the buffered text into spoken audio output.
2. End

Key features:
- Provides offline speech synthesis using `pyttsx3`.
- Can be integrated with different voice profiles for customization.

# 5. Graphical User Interface Module (GUI)

The GUI Module provides an interactive interface for users who prefer visual feedback over voice commands.

**Algorithm V: Graphical User Interface (GUI) Execution Workflow**
- Input: User-provided text command via GUI input field.
- Output: The corresponding action is executed, and a response dialog is displayed.

Steps:
1. Begin
2. Initialize the main application window.
3. Set an appropriate window title that clearly reflects the assistant's role.
4. Design an input element that allows the user to enter textual commands.
5. Integrate an interactive control labeled "Execute" that triggers the callback.
6. Define `on_submit()`:
   a. Retrieve the text entered in the input field.
   b. Forward the text to the intent recognition module.
   c. Send the recognized intent and original command to the command execution module.
   d. Present a dialog box that confirms the recognized intent and result.
7. Render the input field and the control button in the layout.
8. Start the GUI event loop.
9. End

Key features:
- Tkinter-based GUI for user-friendly interaction.
- Provides a text input option for users who prefer typing over speaking.

# 6. System Integration and Execution

All modules are combined in a unified script to ensure seamless interaction between Speech Recognition, NLP, Command Execution, TTS, and GUI.

**Algorithm VI: Integrated Voice Assistant Workflow**
- Objective: Enable uninterrupted monitoring of user speech, identify intent, execute the relevant operation, and deliver audible feedback while preserving GUI responsiveness.

Steps:
1. Begin
2. Initialize and display the graphical user interface in the primary thread.
3. Start a parallel execution thread dedicated to voice-based interactions.
4. Inside the voice thread, loop continuously:
   a. Acquire spoken input via the Speech Recognition Module.
   b. If valid speech is detected:
      i. Forward the transcribed command to the Intent Recognition module.
      ii. Send the inferred intent and user command to the Command Execution module.
      iii. Activate the TTS engine to produce audible feedback.
5. Ensure both GUI and voice threads run concurrently.
6. End

Key features:
- Uses multithreading to separate the speech recognition engine from the GUI and prevent interface lag.
- Supports continuous voice monitoring for seamless user interaction.



