"""Command-line interface for VoiceLab."""

from __future__ import annotations

import argparse
from pathlib import Path

from .models import TranscriptEntry
from .recognition import RecognitionError, recognise_once, speak
from .storage import TranscriptStore


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description="Record speech, create an auditable transcript, and save it as JSON Lines.")
    command.add_argument("--typed", metavar="TEXT", help="Save typed text instead of using the microphone (useful for demos and tests).")
    command.add_argument("--language", default="en-ZA", help="BCP-47 recognition language, e.g. en-ZA or zu-ZA (default: en-ZA).")
    command.add_argument("--output", default="data/transcripts.jsonl", help="Transcript output path (default: data/transcripts.jsonl).")
    command.add_argument("--calibration", type=float, default=0.7, help="Ambient-noise calibration in seconds (default: 0.7).")
    command.add_argument("--timeout", type=float, default=8, help="Seconds to wait for speech (default: 8).")
    command.add_argument("--phrase-time-limit", type=float, default=20, help="Maximum phrase duration in seconds (default: 20).")
    command.add_argument("--speak", action="store_true", help="Read the final transcript aloud.")
    command.add_argument("--history", action="store_true", help="Print saved transcript history and exit.")
    return command


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    store = TranscriptStore(Path(args.output))
    if args.history:
        records = store.read_all()
        if not records:
            print("No saved transcripts yet.")
            return 0
        for record in records:
            print(f"[{record.created_at}] ({record.language}, {record.source}) {record.text}")
        return 0
    if args.calibration < 0:
        parser().error("--calibration must be zero or greater")
    try:
        if args.typed is not None:
            text, source = args.typed, "typed"
        else:
            text = recognise_once(args.language, args.calibration, args.timeout, args.phrase_time_limit)
            source = "microphone"
        entry = TranscriptEntry.create(text=text, source=source, language=args.language)
        store.append(entry)
        print(f"Transcript: {entry.text}")
        print(f"Saved to: {store.path}")
        if args.speak:
            speak(entry.text)
    except (RecognitionError, ValueError) as error:
        print(f"VoiceLab error: {error}")
        return 1
    return 0
