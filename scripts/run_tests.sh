#!/usr/bin/env bash
set -euo pipefail

echo "Running backend tests"
(cd backend && python -m pytest)

echo "Frontend tests are placeholders; add jest or playwright suites in frontend/src/tests or frontend/e2e."
