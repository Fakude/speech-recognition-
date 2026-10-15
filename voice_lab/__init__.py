"""VoiceLab: a small, auditable speech-to-text application."""

from .models import TranscriptEntry
from .storage import TranscriptStore

__all__ = ["TranscriptEntry", "TranscriptStore"]
