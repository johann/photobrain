#!/usr/bin/env bash
set -euo pipefail

echo "Creating PhotoBrain directory layout at /Volumes/PhotoVault"
mkdir -p /Volumes/PhotoVault/{_ingest,_processing,_exports,library/{raw,keepers,maybes,rejects,duplicates,jpg,previews,lightroom-ready},metadata/{xmp,json,db},timelapse,logs,web}

echo "Copying launch agents"
mkdir -p ~/Library/LaunchAgents
cp ./launchd/com.photobrain.*.plist ~/Library/LaunchAgents/
