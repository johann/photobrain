"""Simulated SD card ingest script.

In a production build this would mount an SD card, copy RAW files into
`_ingest`, rename them, and initialize DB entries.
"""
from pathlib import Path

from backend.app.core.config import settings


def ingest(source: Path) -> Path:
    ingest_root = settings.photovault_root / "_ingest"
    destination = ingest_root / source.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("placeholder")
    return destination


if __name__ == "__main__":
    created = ingest(Path("/Volumes/SDCARD/session1"))
    print(f"Ingested to {created}")
