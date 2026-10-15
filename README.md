# VoiceLab

VoiceLab is a small, auditable speech-to-text application. It captures one phrase at a time, stores transcripts in JSON Lines format, and includes a typed mode so the project can be demonstrated without microphone hardware.

## Features

- Microphone transcription through Google Speech Recognition
- South African English as the default recognition language (`en-ZA`)
- Ambient-noise calibration, speech timeout, and phrase-duration controls
- Clear errors for missing microphones, unintelligible audio, missing packages, and network failures
- Append-only JSON Lines transcript storage for later data analysis
- Typed demonstration mode and a transcript-history viewer
- Optional text-to-speech playback
- Unit tests for the core storage and validation behaviour

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Speak when the application prints `Listening…`. A recognised phrase is saved to `data/transcripts.jsonl`.

## Demonstrate without a microphone

```bash
python app.py --typed "Good morning, VoiceLab" --output data/demo.jsonl
python app.py --history --output data/demo.jsonl
```

## Useful options

```bash
python app.py --language en-ZA --timeout 10 --phrase-time-limit 25
python app.py --typed "Sawubona" --language zu-ZA --speak
```

`SpeechRecognition` sends audio to Google's recognition service in microphone mode, so an internet connection is required. The application does not make a network request in `--typed` mode.

## Test

```bash
python -m unittest discover -s tests -v
```

## Project structure

```text
app.py                 # command-line entry point
voice_lab/             # models, storage, recognition adapter, CLI
tests/                 # unit tests
data/                  # local transcript output (ignored by Git)
```

## Continuous integration

[![Python CI](https://github.com/Fakude/speech-recognition-/actions/workflows/ci.yml/badge.svg)](https://github.com/Fakude/speech-recognition-/actions/workflows/ci.yml)

Every push and pull request installs the pinned dependencies and runs the unit-test suite on Python 3.12. The workflow is defined in `.github/workflows/ci.yml`.
