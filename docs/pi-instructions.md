# PhotoBrain Raspberry Pi 5 Setup Instructions

These steps prepare a Raspberry Pi 5 running 64-bit Raspberry Pi OS (Bookworm) to ingest and process photos with PhotoBrain. The guide assumes you will attach a single external drive and run the services headless.

## 1) Prep the Pi and external drive
1. Fully update the OS and reboot:
   ```bash
   sudo apt update && sudo apt full-upgrade -y
   sudo reboot
   ```
2. Enable SSH for headless access: **sudo raspi-config → Interface Options → SSH → Enable**.
3. Attach and format your external drive (ext4 recommended). Mount it persistently at `/mnt/PhotoVault` by adding an `/etc/fstab` entry. Example fstab line (replace `UUID` with your drive's):
   ```
   UUID=<drive-uuid> /mnt/PhotoVault ext4 defaults,noatime 0 2
   ```
   After editing fstab, create the mountpoint and mount:
   ```bash
   sudo mkdir -p /mnt/PhotoVault
   sudo mount -a
   ```

## 2) Install required packages
1. Install core dependencies and toolchain:
   ```bash
   sudo apt install -y git ffmpeg exiftool python3-venv python3-pip build-essential
   ```
2. Install Node.js 18 via NodeSource (Bookworm's repo may lag behind):
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt install -y nodejs
   ```
3. Optional RAW processor: install Darktable (heavier) or RawTherapee (lighter) depending on preference:
   ```bash
   sudo apt install -y darktable   # or: sudo apt install -y rawtherapee
   ```

## 3) Fetch the code onto the external drive
1. Place the repo on the mounted drive so all data stays with the disk:
   ```bash
   sudo mkdir -p /mnt/PhotoVault/web
   sudo chown -R $(whoami):$(whoami) /mnt/PhotoVault/web
   cd /mnt/PhotoVault/web
   git clone <your-photobrain-repo-url> photobrain
   cd photobrain
   ```

## 4) Configure environment variables
1. Copy the example environment file and keep paths aligned with the `/mnt/PhotoVault` mount:
   ```bash
   cp .env.example .env
   ```
2. Ensure these values point at the mounted drive (adjust if you chose a different path):
   ```
   PB_PHOTOVAULT_ROOT=/mnt/PhotoVault
   PB_DB_PATH=/mnt/PhotoVault/metadata/db/photobrain.db
   PB_RAW_PROCESSOR=darktable   # or rawtherapee if installed above
   ```

## 5) Install backend dependencies (FastAPI)
1. Create and activate a Python virtual environment in the repo root:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install backend dependencies from the `backend/` directory (include dev extras for tooling/tests):
   ```bash
   cd backend
   pip install -e .[dev]
   cd ..
   ```

## 6) Install frontend dependencies (Next.js)
1. Install Node packages for the frontend:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

## 7) Run PhotoBrain on the Pi
- For interactive development (shell attached), start both services from the repo root:
  ```bash
  bash scripts/dev_start.sh
  ```
  This launches the FastAPI backend on port 8000 and the Next.js frontend on port 3000.
- For headless/automatic operation, create a `systemd` service and timer to run your ingest/processing scripts on a schedule. A simple starting point is a user timer that triggers the process script every 15 minutes. Example unit files (place under `~/.config/systemd/user/`):
  - `photobrain-process.service`:
    ```ini
    [Unit]
    Description=PhotoBrain process pipeline

    [Service]
    WorkingDirectory=%h/../mnt/PhotoVault/web/photobrain
    ExecStart=%h/../mnt/PhotoVault/web/photobrain/scripts/dev_start.sh
    Restart=on-failure
    Environment=PB_PHOTOVAULT_ROOT=/mnt/PhotoVault
    Environment=PB_DB_PATH=/mnt/PhotoVault/metadata/db/photobrain.db
    Environment=PB_RAW_PROCESSOR=darktable
    ```
  - `photobrain-process.timer`:
    ```ini
    [Unit]
    Description=Run PhotoBrain pipeline every 15 minutes

    [Timer]
    OnBootSec=2min
    OnUnitActiveSec=15min
    Unit=photobrain-process.service

    [Install]
    WantedBy=default.target
    ```
  Enable and start the timer after creating both files:
  ```bash
  systemctl --user daemon-reload
  systemctl --user enable --now photobrain-process.timer
  ```
  Adjust the unit `WorkingDirectory` if your mount point differs.

## 8) Verify everything works
1. Browse to `http://<pi-hostname>.local:3000` on your LAN after starting the frontend.
2. Check logs under `/mnt/PhotoVault/logs` (create the folder if missing) for ingest/processing activity.
3. Inspect systemd state to confirm the timer is active and recent runs succeeded:
   ```bash
   systemctl --user status photobrain-process.timer
   journalctl --user -u photobrain-process.service --since "-15 minutes"
   ```

## 9) Keep the system up to date
1. Pull new code periodically:
   ```bash
   cd /mnt/PhotoVault/web/photobrain
   git pull
   ```
2. Re-run `pip install -e .[dev]` in `backend/` and `npm install` in `frontend/` when dependencies change.
3. After modifying your systemd units or scripts, reload the daemon and restart the timer:
   ```bash
   systemctl --user daemon-reload
   systemctl --user restart photobrain-process.timer
   ```

Following these steps gives you a headless Raspberry Pi 5 host that runs PhotoBrain from your external drive and keeps data and compute together for easy portability.
