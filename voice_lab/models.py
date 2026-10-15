"""Domain models used by VoiceLab."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class TranscriptEntry:
    """One recognised or manually entered piece of speech."""

    text: str
    source: str
    language: str
    created_at: str

    @classmethod
    def create(cls, text: str, source: str, language: str) -> "TranscriptEntry":
        clean_text = " ".join(text.split())
        if not clean_text:
            raise ValueError("A transcript cannot be empty.")
        return cls(
            text=clean_text,
            source=source,
            language=language,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

    def to_dict(self) -> dict[str, str]:
        return asdict(self)
