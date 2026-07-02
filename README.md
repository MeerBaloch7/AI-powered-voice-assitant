# Speech Recognition Module

A Python-based Speech-to-Text (STT) conversion module that leverages multiple recognition engines for robust audio transcription capabilities.

## Overview

This module provides a comprehensive speech recognition solution that attempts transcription using Google's Speech Recognition API with fallback support to CMU Sphinx for offline functionality. It's designed to handle ambient noise and deliver reliable text conversion from audio input.

## Prerequisites

Before installing this module, ensure you have:
- Python 3.7 or higher
- A working microphone connected to your system
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
pip install pocketsphinx
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
     Google Speech Recognition
          │                  │
        Success            Failure
          │                  │
          ▼                  ▼
    Return Text      CMU Sphinx Recognition
                         │
                  ┌──────┴──────┐
               Success       Failure
                  │              │
                  ▼              ▼
           Return Text     Return Error
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.



