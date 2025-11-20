import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from ..core.config import settings
from ..models.domain import JobStatus, Photo, Shoot, Timelapse

CATALOG_FILENAME = "catalog.json"


def _metadata_dir() -> Path:
    return settings.photovault_root / "metadata" / "json"


def _catalog_path() -> Path:
    return _metadata_dir() / CATALOG_FILENAME


def _ensure_metadata_dirs() -> None:
    _metadata_dir().mkdir(parents=True, exist_ok=True)


def _load_raw_catalog() -> Dict:
    path = _catalog_path()
    if not path.exists():
        return {"shoots": [], "photos": [], "timelapses": [], "jobs": []}
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return {
        "shoots": data.get("shoots", []),
        "photos": data.get("photos", []),
        "timelapses": data.get("timelapses", []),
        "jobs": data.get("jobs", []),
    }


def _serialize_datetime(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.isoformat()


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _serialize_path(value: Optional[Path]) -> Optional[str]:
    return str(value) if value else None


def _deserialize_path(value: Optional[str]) -> Optional[Path]:
    return Path(value) if value else None


def _save_raw_catalog(data: Dict) -> None:
    _ensure_metadata_dirs()
    path = _catalog_path()
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _as_model_list(raw_items: List[Dict], model_cls):
    models = []
    for item in raw_items:
        parsed = item.copy()
        if "captured_at" in parsed and isinstance(parsed["captured_at"], str):
            parsed["captured_at"] = _parse_datetime(parsed["captured_at"])
        if "created_at" in parsed and isinstance(parsed["created_at"], str):
            parsed["created_at"] = _parse_datetime(parsed["created_at"])
        if "updated_at" in parsed and isinstance(parsed["updated_at"], str):
            parsed["updated_at"] = _parse_datetime(parsed["updated_at"])
        if "preview_path" in parsed:
            parsed["preview_path"] = _deserialize_path(parsed.get("preview_path"))
        if "video_path" in parsed:
            parsed["video_path"] = _deserialize_path(parsed.get("video_path"))
        if "log_path" in parsed:
            parsed["log_path"] = _deserialize_path(parsed.get("log_path"))
        models.append(model_cls(**parsed))
    return models


def _export_models(items: List) -> List[Dict]:
    exported = []
    for item in items:
        data = item.dict()
        for key in ("captured_at", "created_at", "updated_at"):
            if key in data and isinstance(data[key], datetime):
                data[key] = _serialize_datetime(data[key])
        if "preview_path" in data:
            data["preview_path"] = _serialize_path(data.get("preview_path"))
        if "video_path" in data:
            data["video_path"] = _serialize_path(data.get("video_path"))
        if "log_path" in data:
            data["log_path"] = _serialize_path(data.get("log_path"))
        exported.append(data)
    return exported


def load_shoots() -> List[Shoot]:
    raw_catalog = _load_raw_catalog()
    return _as_model_list(raw_catalog["shoots"], Shoot)


def load_photos() -> List[Photo]:
    raw_catalog = _load_raw_catalog()
    return _as_model_list(raw_catalog["photos"], Photo)


def load_timelapses() -> List[Timelapse]:
    raw_catalog = _load_raw_catalog()
    return _as_model_list(raw_catalog["timelapses"], Timelapse)


def load_jobs() -> List[JobStatus]:
    raw_catalog = _load_raw_catalog()
    return _as_model_list(raw_catalog["jobs"], JobStatus)


def get_shoot(shoot_id: str) -> Optional[Shoot]:
    return next((shoot for shoot in load_shoots() if shoot.id == shoot_id), None)


def get_photo(photo_id: str) -> Optional[Photo]:
    return next((photo for photo in load_photos() if photo.id == photo_id), None)


def get_timelapse(timelapse_id: str) -> Optional[Timelapse]:
    return next((tl for tl in load_timelapses() if tl.id == timelapse_id), None)


def update_photo(photo_id: str, rating: Optional[int], labels: Optional[List[str]]) -> Optional[Photo]:
    photos = load_photos()
    target = None
    for idx, photo in enumerate(photos):
        if photo.id == photo_id:
            updated = photo.copy(update={
                "rating": rating if rating is not None else photo.rating,
                "labels": labels if labels is not None else photo.labels,
            })
            photos[idx] = updated
            target = updated
            break
    if target is None:
        return None

    catalog = _load_raw_catalog()
    catalog["photos"] = _export_models(photos)
    _save_raw_catalog(catalog)
    return target


def create_timelapse(timelapse: Timelapse) -> Timelapse:
    existing = load_timelapses()
    ids = {tl.id for tl in existing}
    if timelapse.id in ids:
        raise ValueError("Timelapse with this id already exists")
    updated = existing + [timelapse]
    catalog = _load_raw_catalog()
    catalog["timelapses"] = _export_models(updated)
    _save_raw_catalog(catalog)
    return timelapse


def queue_job(name: str, status: str = "queued") -> JobStatus:
    now = datetime.now(timezone.utc)
    job = JobStatus(
        id=f"job-{int(now.timestamp())}",
        name=name,
        status=status,
        created_at=now,
        updated_at=now,
        log_path=settings.photovault_root / "logs" / f"{name.replace(' ', '-').lower()}.log",
    )
    jobs = load_jobs() + [job]
    catalog = _load_raw_catalog()
    catalog["jobs"] = _export_models(jobs)
    _save_raw_catalog(catalog)
    return job


def list_jobs() -> List[JobStatus]:
    return load_jobs()


def get_job(job_id: str) -> Optional[JobStatus]:
    return next((job for job in load_jobs() if job.id == job_id), None)


def disk_usage() -> Dict[str, float]:
    root = settings.photovault_root
    if not root.exists():
        return {"root": str(root), "used_gb": 0.0, "free_gb": 0.0}
    usage = shutil.disk_usage(root)
    gb = 1024 * 1024 * 1024
    return {
        "root": str(root),
        "used_gb": round(usage.used / gb, 2),
        "free_gb": round(usage.free / gb, 2),
    }
