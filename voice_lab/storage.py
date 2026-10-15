"""Append-only transcript storage."""

from __future__ import annotations

import json
from pathlib import Path

from .models import TranscriptEntry


class TranscriptStore:
    """Save transcripts as JSON Lines, a simple format for later analysis."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def append(self, entry: TranscriptEntry) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(entry.to_dict(), ensure_ascii=False) + "\n")

    def read_all(self) -> list[TranscriptEntry]:
        if not self.path.exists():
            return []
        entries: list[TranscriptEntry] = []
        with self.path.open(encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                if not line.strip():
                    continue
                try:
                    entries.append(TranscriptEntry(**json.loads(line)))
                except (json.JSONDecodeError, TypeError) as error:
                    raise ValueError(f"Invalid record on line {line_number} in {self.path}") from error
        return entries
