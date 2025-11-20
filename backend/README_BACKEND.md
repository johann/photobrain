# PhotoBrain Backend

A FastAPI service that exposes the core API for PhotoBrain. Endpoints mirror the specification in the root README.

## Running locally

```bash
uvicorn backend.app.main:app --reload --port 8000
```

## Testing

```bash
python -m pytest
```

## Configuration

Environment variables:

- `PB_PHOTOVAULT_ROOT` (default: `/Volumes/PhotoVault`)
- `PB_DB_PATH` (default: `/Volumes/PhotoVault/metadata/db/photobrain.db`)
- `PB_RAW_PROCESSOR` (default: `darktable`)
- `NEXT_PUBLIC_API_BASE_URL` (default: `http://localhost:8000`)
