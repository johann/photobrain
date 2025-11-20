from fastapi import APIRouter, HTTPException

from ..models.domain import JobStatus, Photo, Shoot, Timelapse
from ..services import mock_data

router = APIRouter(prefix="/api")


@router.get("/shoots", response_model=list[Shoot])
def list_shoots() -> list[Shoot]:
    return list(mock_data.SHOOTS.values())


@router.get("/shoots/{shoot_id}", response_model=Shoot)
def get_shoot(shoot_id: str) -> Shoot:
    shoot = mock_data.SHOOTS.get(shoot_id)
    if not shoot:
        raise HTTPException(status_code=404, detail="Shoot not found")
    return shoot


@router.post("/shoots/reindex", response_model=dict)
def reindex_shoots() -> dict:
    return {"status": "queued", "job": "reindex"}


@router.post("/shoots/{shoot_id}/reprocess", response_model=dict)
def reprocess_shoot(shoot_id: str) -> dict:
    if shoot_id not in mock_data.SHOOTS:
        raise HTTPException(status_code=404, detail="Shoot not found")
    return {"status": "queued", "job": f"reprocess:{shoot_id}"}


@router.get("/photos", response_model=list[Photo])
def list_photos() -> list[Photo]:
    return list(mock_data.PHOTOS.values())


@router.get("/photos/{photo_id}", response_model=Photo)
def get_photo(photo_id: str) -> Photo:
    photo = mock_data.PHOTOS.get(photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo


@router.get("/photos/{photo_id}/image", response_model=dict)
def get_photo_image(photo_id: str) -> dict:
    photo = mock_data.PHOTOS.get(photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return {"path": str(photo.preview_path)}


@router.patch("/photos/{photo_id}", response_model=Photo)
def update_photo(photo_id: str, rating: int | None = None, labels: list[str] | None = None) -> Photo:
    photo = mock_data.PHOTOS.get(photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    updated = photo.copy(update={
        "rating": rating if rating is not None else photo.rating,
        "labels": labels if labels is not None else photo.labels,
    })
    mock_data.PHOTOS[photo_id] = updated
    return updated


@router.get("/timelapses", response_model=list[Timelapse])
def list_timelapses() -> list[Timelapse]:
    return list(mock_data.TIMELAPSES.values())


@router.get("/timelapses/{timelapse_id}", response_model=Timelapse)
def get_timelapse(timelapse_id: str) -> Timelapse:
    timelapse = mock_data.TIMELAPSES.get(timelapse_id)
    if not timelapse:
        raise HTTPException(status_code=404, detail="Timelapse not found")
    return timelapse


@router.post("/timelapses", response_model=Timelapse, status_code=201)
def create_timelapse(timelapse: Timelapse) -> Timelapse:
    mock_data.TIMELAPSES[timelapse.id] = timelapse
    return timelapse


@router.get("/timelapses/{timelapse_id}/video", response_model=dict)
def get_timelapse_video(timelapse_id: str) -> dict:
    timelapse = mock_data.TIMELAPSES.get(timelapse_id)
    if not timelapse:
        raise HTTPException(status_code=404, detail="Timelapse not found")
    return {"path": str(timelapse.video_path)}


@router.get("/system/health", response_model=dict)
def system_health() -> dict:
    return {"status": "ok"}


@router.get("/system/disk-usage", response_model=dict)
def system_disk_usage() -> dict:
    return {
        "root": "/Volumes/PhotoVault",
        "used_gb": 128,
        "free_gb": 872,
    }


@router.get("/system/jobs", response_model=list[JobStatus])
def list_jobs() -> list[JobStatus]:
    return mock_data.JOBS


@router.get("/system/jobs/{job_id}", response_model=JobStatus)
def get_job(job_id: str) -> JobStatus:
    for job in mock_data.JOBS:
        if job.id == job_id:
            return job
    raise HTTPException(status_code=404, detail="Job not found")
