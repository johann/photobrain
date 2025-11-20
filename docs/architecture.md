# Architecture

PhotoBrain is split into a FastAPI backend, a Next.js frontend, and a lightweight pipeline layer for ingest and processing. The backend serves JSON APIs for shoots, photos, timelapses, and system health. The frontend consumes these APIs and renders galleries and dashboards. Pipeline scripts move files through the `/Volumes/PhotoVault` layout.
