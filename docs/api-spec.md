# API Specification (snapshot)

The FastAPI backend exposes endpoints under `/api`:

- `GET /api/shoots` — list shoots
- `GET /api/shoots/{id}` — fetch single shoot
- `POST /api/shoots/reindex` — queue reindex job
- `POST /api/shoots/{id}/reprocess` — queue reprocess job
- `GET /api/photos` — list photos
- `GET /api/photos/{id}` — fetch single photo
- `GET /api/photos/{id}/image` — return preview path
- `PATCH /api/photos/{id}` — update rating/labels
- `GET /api/timelapses` — list timelapses
- `GET /api/timelapses/{id}` — fetch timelapse
- `POST /api/timelapses` — create timelapse
- `GET /api/timelapses/{id}/video` — return video path
- `GET /api/system/health` — health check
- `GET /api/system/disk-usage` — disk usage summary
- `GET /api/system/jobs` — list jobs
- `GET /api/system/jobs/{id}` — fetch job status
