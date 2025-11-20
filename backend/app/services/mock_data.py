from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

from ..models.domain import JobStatus, Photo, Shoot, Timelapse

now = datetime.utcnow()

SHOOTS: Dict[str, Shoot] = {
    "shoot-1": Shoot(
        id="shoot-1",
        name="Golden Gate Fog",
        captured_at=now - timedelta(days=1),
        location="San Francisco, CA",
        tags=["fog", "bridge", "sunrise"],
    ),
    "shoot-2": Shoot(
        id="shoot-2",
        name="Night City",
        captured_at=now - timedelta(days=2),
        location="Tokyo",
        tags=["night", "city"],
    ),
}

PHOTOS: Dict[str, Photo] = {
    "photo-1": Photo(
        id="photo-1",
        shoot_id="shoot-1",
        filename="DSC0001.RAW",
        captured_at=now - timedelta(days=1, hours=1),
        rating=4,
        labels=["fog", "bridge"],
        preview_path=Path("/Volumes/PhotoVault/library/previews/photo-1.jpg"),
    ),
    "photo-2": Photo(
        id="photo-2",
        shoot_id="shoot-1",
        filename="DSC0002.RAW",
        captured_at=now - timedelta(days=1, hours=1, minutes=10),
        rating=3,
        labels=["sunrise"],
        preview_path=Path("/Volumes/PhotoVault/library/previews/photo-2.jpg"),
    ),
    "photo-3": Photo(
        id="photo-3",
        shoot_id="shoot-2",
        filename="DSC1001.RAW",
        captured_at=now - timedelta(days=2, hours=3),
        rating=5,
        labels=["city", "night"],
        preview_path=Path("/Volumes/PhotoVault/library/previews/photo-3.jpg"),
    ),
}

TIMELAPSES: Dict[str, Timelapse] = {
    "tl-1": Timelapse(
        id="tl-1",
        title="Fog Rolling In",
        shoot_ids=["shoot-1"],
        frame_count=240,
        video_path=Path("/Volumes/PhotoVault/timelapse/tl-1.mp4"),
    )
}

JOBS: List[JobStatus] = [
    JobStatus(
        id="job-1",
        name="Ingest SD Card",
        status="completed",
        created_at=now - timedelta(hours=4),
        updated_at=now - timedelta(hours=3, minutes=45),
        log_path=Path("/Volumes/PhotoVault/logs/job-1.log"),
    ),
    JobStatus(
        id="job-2",
        name="Process New Photos",
        status="running",
        created_at=now - timedelta(minutes=30),
        updated_at=now - timedelta(minutes=5),
        log_path=Path("/Volumes/PhotoVault/logs/job-2.log"),
    ),
]
