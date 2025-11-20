#!/usr/bin/env bash
set -euo pipefail

# start backend
uvicorn backend.app.main:app --reload --port 8000 &
BACKEND_PID=$!

# start frontend
(cd frontend && npm install && npm run dev) &
FRONTEND_PID=$!

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
