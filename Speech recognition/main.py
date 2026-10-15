"""Compatibility launcher for the original project location."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from voice_lab.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
    
