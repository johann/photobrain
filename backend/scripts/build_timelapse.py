"""Stub timelapse builder.

A real implementation would use ffmpeg; this just writes a marker file.
"""
from pathlib import Path

from backend.app.core.config import settings


def build(source_frames: list[Path], name: str) -> Path:
    timelapse_root = settings.photovault_root / "timelapse"
    timelapse_root.mkdir(parents=True, exist_ok=True)
    output = timelapse_root / f"{name}.mp4"
    output.write_text("timelapse placeholder")
    return output


if __name__ == "__main__":
    video = build([Path("/Volumes/PhotoVault/library/jpg/photo-1.jpg")], "demo")
    print(f"Generated timelapse at {video}")
