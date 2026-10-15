"""Tests for the persistence layer."""

import tempfile
import unittest
from pathlib import Path

from voice_lab.models import TranscriptEntry
from voice_lab.storage import TranscriptStore


class TranscriptStoreTests(unittest.TestCase):
    def test_append_and_read_a_transcript(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = TranscriptStore(Path(directory) / "transcripts.jsonl")
            store.append(TranscriptEntry.create("  Hello   world ", "typed", "en-ZA"))
            records = store.read_all()
        self.assertEqual(records[0].text, "Hello world")
        self.assertEqual(records[0].source, "typed")

    def test_empty_text_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            TranscriptEntry.create("  ", "typed", "en-ZA")


if __name__ == "__main__":
    unittest.main()
