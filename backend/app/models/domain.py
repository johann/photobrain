from datetime import datetime
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel


class Shoot(BaseModel):
    id: str
    name: str
    captured_at: datetime
    location: Optional[str] = None
    tags: List[str] = []


class Photo(BaseModel):
    id: str
    shoot_id: str
    filename: str
    captured_at: datetime
    rating: Optional[int] = None
    labels: List[str] = []
    preview_path: Optional[Path] = None


class Timelapse(BaseModel):
    id: str
    title: str
    shoot_ids: List[str]
    frame_count: int
    video_path: Optional[Path] = None


class JobStatus(BaseModel):
    id: str
    name: str
    status: str
    created_at: datetime
    updated_at: datetime
    log_path: Optional[Path] = None
