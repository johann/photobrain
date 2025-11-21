# PhotoBrain MacBook Setup Instructions

This walkthrough assumes you are preparing the Intel MacBook Pro described in the project brief (external screen only, single external drive at `/Volumes/PhotoVault`). Follow the steps in order on the Mac itself.

## 1) Prepare the Mac and external drive
1. Connect the `/Volumes/PhotoVault` drive and make sure it mounts at that exact path. Rename the volume to `PhotoVault` if needed.
2. Enable remote access if you plan to work headless: **System Settings → General → Sharing → Remote Login** (SSH) and **Screen Sharing**.
3. Install Xcode Command Line Tools if they are missing:
   ```bash
   xcode-select --install
   ```

## 2) Install required packages
1. Install Homebrew if you do not already have it:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Use Homebrew to install the dependencies PhotoBrain expects:
   ```bash
   brew install python@3.11 node@18 git ffmpeg exiftool darktable
   ```
   - If you prefer RawTherapee instead of Darktable, install `rawtherapee` and set `PB_RAW_PROCESSOR=rawtherapee` later.
3. Ensure `python3` and `node` resolve to the Homebrew versions in new shells (you may need to add Homebrew’s `bin` paths to `PATH`).

## 3) Fetch the code to the external drive
1. Create the project root on the external drive and clone the repo there so the launch agents can find it:
   ```bash
   mkdir -p /Volumes/PhotoVault/web
   cd /Volumes/PhotoVault/web
   git clone <your-photobrain-repo-url> photobrain
   cd photobrain
   ```

## 4) Create the PhotoBrain folder layout and install launch agents
1. Run the bootstrap script from the repo root to create the required directory tree on the external drive and copy the launch agent plist files into your user LaunchAgents folder:
   ```bash
   bash scripts/bootstrap_macos.sh
   ```
2. Load the launch agents so they start automatically (they point at `/Volumes/PhotoVault/web/...`):
   ```bash
   launchctl load ~/Library/LaunchAgents/com.photobrain.ingest.plist
   launchctl load ~/Library/LaunchAgents/com.photobrain.process.plist
   launchctl load ~/Library/LaunchAgents/com.photobrain.maintenance.plist
   ```
   - The ingest agent runs on load, the process agent runs every 15 minutes, and the maintenance agent runs nightly at 3:00 AM.

## 5) Configure environment variables
1. Copy the example environment file and adjust values if needed:
   ```bash
   cp .env.example .env
   ```
2. Leave `PB_PHOTOVAULT_ROOT` and `PB_DB_PATH` pointing to `/Volumes/PhotoVault` unless you deliberately changed the mount point.
3. Set `PB_RAW_PROCESSOR` to `darktable` (default) or `rawtherapee` to match the software you installed.

## 6) Install backend dependencies (FastAPI)
1. Create and activate a Python virtual environment in the repo root:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install the backend (and dev tools for tests) from the `backend/` directory:
   ```bash
   cd backend
   pip install -e .[dev]
   cd ..
   ```

## 7) Install frontend dependencies (Next.js)
1. Install Node packages for the frontend:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

## 8) Run PhotoBrain locally
- For development, start both services with the helper script from the repo root:
  ```bash
  bash scripts/dev_start.sh
  ```
  This launches the FastAPI backend on port 8000 and the Next.js frontend on port 3000.
- For headless/automatic use, rely on the launch agents loaded earlier; they will execute the ingestion, processing, and maintenance workflows using the scripts in `/Volumes/PhotoVault/web/backend/scripts/` and `/Volumes/PhotoVault/web/scripts/`.

## 9) Verify everything works
1. Visit `http://<host>.local:3000` on your LAN to load the web UI once the frontend is running.
2. Check logs under `/Volumes/PhotoVault/logs` for ingest/processing activity.
3. Use `launchctl list | grep photobrain` to confirm the agents are loaded and look for any last-exit-status errors.

## 10) Keeping the system up to date
1. Pull new code periodically:
   ```bash
   cd /Volumes/PhotoVault/web/photobrain
   git pull
   ```
2. Re-run `pip install -e .[dev]` in `backend/` and `npm install` in `frontend/` when dependencies change.
3. Reload launch agents after plist or script changes:
   ```bash
   launchctl unload ~/Library/LaunchAgents/com.photobrain.ingest.plist
   launchctl unload ~/Library/LaunchAgents/com.photobrain.process.plist
   launchctl unload ~/Library/LaunchAgents/com.photobrain.maintenance.plist
   launchctl load ~/Library/LaunchAgents/com.photobrain.ingest.plist
   launchctl load ~/Library/LaunchAgents/com.photobrain.process.plist
   launchctl load ~/Library/LaunchAgents/com.photobrain.maintenance.plist
   ```

If you follow these steps in order, your headless MacBook should ingest SD cards, process photos, and expose the PhotoBrain UI over your local network with minimal manual intervention.
