"""Stub for processing new photos.

This would normally invoke RAW processing, ML culling, and preview generation.
"""
from pathlib import Path

from backend.app.core.config import settings


def process(session_path: Path) -> Path:
    processed_root = settings.photovault_root / "_processing"
    processed = processed_root / session_path.name
    processed.parent.mkdir(parents=True, exist_ok=True)
    processed.write_text("processed")
    return processed


if __name__ == "__main__":
    output = process(Path(settings.photovault_root / "_ingest/session1"))
    print(f"Processed session at {output}")
