# PhotoBrain: Headless Photography Workflow Appliance

A headless, automated photography workflow system designed for an Intel MacBook Pro with a broken screen and a **single external hard drive**, with a clear path to expand to a multi-drive enclosure later.

This project includes:

- A **FastAPI backend** (Python)
- A **Next.js frontend**
- A **background pipeline layer** (Python)
- A **testing setup** for backend + frontend, including E2E
- macOS **launch agents** to make the system fully automatic

This README is the full specification for the repository that Codex (or any generator) will implement.

## 1. High-Level Goals

1. Use an old Intel MacBook Pro as a headless photography server.
2. Store all data on a single external drive (`/Volumes/PhotoVault`).
3. Automate:
   - SD card ingest
   - RAW renaming
   - ML-assisted culling
   - RAW→JPG processing
   - preview generation
   - metadata extraction
   - timelapse creation
4. Provide a LAN-only web UI for browsing, filtering, and inspecting photos.
5. Offer a clean path for future expansion.
6. Enforce a strong testing discipline for backend + frontend.

## 2. Physical Setup

- Host: Intel MacBook Pro with a broken screen.
- Single external drive at `/Volumes/PhotoVault`.
- macOS headless (SSH + Screen Sharing enabled).
- Web UI accessible via `http://<host>.local:3000` (frontend) and `http://<host>.local:8000` (API).

## 3. Single-Drive Storage Layout

Everything lives under:

```
/Volumes/PhotoVault
  /_ingest
  /_processing
  /_exports
  /library
    /raw
    /keepers
    /maybes
    /rejects
    /duplicates
    /jpg
    /previews
    /lightroom-ready
  /metadata
    /xmp
    /json
    /db
  /timelapse
  /logs
  /web
```

This structure must be used across the backend, pipeline, DB, and UI.

## 4. Repo Structure

The repository should look like this:

```
.
├─ backend/
│  ├─ app/
│  │  ├─ api/
│  │  ├─ core/
│  │  ├─ models/
│  │  ├─ db/
│  │  ├─ services/
│  │  ├─ workers/
│  │  └─ main.py
│  ├─ scripts/
│  ├─ tests/
│  ├─ pyproject.toml
│  └─ README_BACKEND.md
│
├─ frontend/
│  ├─ src/
│  │  ├─ app/ or pages/
│  │  ├─ components/
│  │  ├─ lib/
│  │  ├─ types/
│  │  └─ tests/
│  ├─ public/
│  ├─ e2e/
│  ├─ package.json
│  └─ README_FRONTEND.md
│
├─ launchd/
│  ├─ com.photobrain.ingest.plist
│  ├─ com.photobrain.process.plist
│  └─ com.photobrain.maintenance.plist
│
├─ docs/
│  ├─ architecture.md
│  ├─ api-spec.md
│  └─ ui-spec.md
│
├─ scripts/
│  ├─ bootstrap_macos.sh
│  ├─ dev_start.sh
│  └─ run_tests.sh
│
├─ .env.example
├─ docker-compose.yml
└─ README.md
```

## 5. Backend Specification (FastAPI)

### Responsibilities

The backend must:

- Expose REST endpoints for shoots, photos, timelapses, jobs, system health.
- Maintain a SQLite database.
- Implement:
  - ingest handling
  - RAW renaming
  - ML-assisted culling
  - RAW→JPG processing
  - preview generation
  - metadata extraction
  - timelapse building
- Expose admin/rebuild endpoints.

### Tech Stack

- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- OpenCV, Mediapipe
- Darktable CLI or RawTherapee CLI
- ExifTool
- Uvicorn

### Database Models

Tables:

- shoots
- photos
- timelapses
- jobs

(Full field definitions unchanged from previous output.)

### Required API Routes

Shoots:
- GET /api/shoots
- GET /api/shoots/{id}
- POST /api/shoots/reindex
- POST /api/shoots/{id}/reprocess

Photos:
- GET /api/photos
- GET /api/photos/{id}
- GET /api/photos/{id}/image
- PATCH /api/photos/{id}

Timelapses:
- GET /api/timelapses
- GET /api/timelapses/{id}
- POST /api/timelapses
- GET /api/timelapses/{id}/video

System:
- GET /api/system/health
- GET /api/system/disk-usage
- GET /api/system/jobs
- GET /api/system/jobs/{id}

### Workers

- Simple SQLite-backed queue.
- Workers poll for queued jobs.
- Jobs write logs to `/Volumes/PhotoVault/logs/`.

## 6. Pipeline Layer

Scripts in `backend/scripts/`:

### ingest_sd_card.py

Handles ingest, renaming, relocation, DB initialization.

### process_new_photos.py

Processes RAWs, runs ML culling, generates JPGs + previews.

### build_timelapse.py

Builds timelapses using ffmpeg.

## 7. Frontend Specification (Next.js)

### Responsibilities

- Render shoots, photos, metadata, filters.
- Provide gallery + detail views.
- Provide timelapse viewer.
- Provide system dashboard.

### Tech Stack

- Next.js 13+ or 14
- TypeScript
- Tailwind
- React Query
- Playwright/Cypress
- Jest/Vitest

### Pages and Components

(Full list kept identical as earlier.)

## 8. macOS Launch Agents

Three agents:
- ingest
- process
- maintenance

All stored in `launchd/`.

## 9. Testing Requirements

### Backend Tests

- pytest
- unit + integration + API
- sample RAWs in `backend/tests/data/`

### Frontend Tests

- unit + integration components
- E2E with Playwright/Cypress

### Combined runner

`scripts/run_tests.sh`

## 10. Environment Configuration

```
PB_PHOTOVAULT_ROOT=/Volumes/PhotoVault
PB_DB_PATH=/Volumes/PhotoVault/metadata/db/photobrain.db
PB_RAW_PROCESSOR=darktable
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## 11. Setup Instructions

- **MacBook walkthrough:** Follow [`docs/instructions.md`](docs/instructions.md) for a step-by-step guide to prepare the Intel MacBook Pro host, install dependencies, and wire up the launch agents.
- **Raspberry Pi 5 walkthrough:** See [`docs/pi-instructions.md`](docs/pi-instructions.md) for end-to-end setup on Raspberry Pi OS, including drive mounting and optional headless systemd scheduling.
- Backend and frontend command references remain unchanged.

## 12. CI Automation

GitHub Actions recommended.

## 13. Future Enhancements

(same list)

## 14. Summary for Codex

Codex must implement:
- backend
- frontend
- pipeline
- tests
- launch agents
- environment configs
- documentation

