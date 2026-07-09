# AGENTS — AI assistant instructions for this repo

Purpose
- Short guidance for coding agents (Copilot-style) to be immediately productive in this workspace.

Quick facts
- **Python:** 3.10+
- **Main entry:** `SRM.py` — contains `SpeechRecognitionModule` with `recognize_speech()`.
- **Dependencies:** See README.md; primary packages: `SpeechRecognition`, `PyAudio`, `pocketsphinx`.

How to run (local, interactive)
- Create and activate a virtual environment, then install dependencies from README.md.

Example (Windows)
```
python -m venv venv
venv\Scripts\activate
pip install SpeechRecognition PyAudio pocketsphinx
python SRM.py
```

What agents should do first
- Read [README.md](README.md) for project overview and installation notes.
- Open [SRM.py](SRM.py) to inspect the `SpeechRecognitionModule` implementation.
- Do not assume tests or CI exist; ask to add them if needed.

Important implementation notes
- `SRM.py` uses the system microphone and external services (Google, Sphinx). Expect environment-specific issues:
  - On Windows, installing `PyAudio` often requires prebuilt wheels; advise the user if pip install fails.
  - Microphone permissions and availability may cause `OSError` — handle gracefully and surface actionable errors.
- Prefer non-blocking edits: add config flags for timeouts, API keys, and an option to read from an audio file for testing.
- Avoid committing large binary audio files to the repo; use fixtures under a dedicated `tests/fixtures` folder if needed.

Testing guidance for agents
- Unit-test logic that doesn't require live audio (parsing, fallback decision, error handling).
- For audio input, add small sample WAV files and tests that use `Recognizer.record()` on files instead of `Microphone`.

Suggested next customizations
- Add `requirements.txt` or `pyproject.toml` listing exact dependency versions.
- Add a small `tests/` suite and CI workflow that runs unit tests without requiring a microphone.
- Consider a `.github/copilot-instructions.md` only if you want a separate GitHub-specific agent instruction file.

Contacts / Context
- The README contains detailed installation steps and architectural notes: [README.md](README.md).

Revision history
- Created AGENTS.md to provide concise, link-first guidance for AI coding agents.
