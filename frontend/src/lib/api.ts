import { DiskUsage, HealthStatus, JobStatus, Photo, Shoot, Timelapse } from "../types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api";

async function fetchJson<T>(path: string): Promise<T> {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`Request failed: ${res.status}`);
  }
  return res.json();
}

export async function getShoots(): Promise<Shoot[]> {
  try {
    return await fetchJson<Shoot[]>("/shoots");
  } catch (error) {
    console.error("Failed to load shoots", error);
    return [];
  }
}

export async function getPhotos(): Promise<Photo[]> {
  try {
    return await fetchJson<Photo[]>("/photos");
  } catch (error) {
    console.error("Failed to load photos", error);
    return [];
  }
}

export async function getTimelapses(): Promise<Timelapse[]> {
  try {
    return await fetchJson<Timelapse[]>("/timelapses");
  } catch (error) {
    console.error("Failed to load timelapses", error);
    return [];
  }
}

export async function getSystemHealth(): Promise<JobStatus[]> {
  try {
    return await fetchJson<JobStatus[]>("/system/jobs");
  } catch (error) {
    console.error("Failed to load jobs", error);
    return [];
  }
}

export async function getHealthStatus(): Promise<HealthStatus | null> {
  try {
    return await fetchJson<HealthStatus>("/system/health");
  } catch (error) {
    console.error("Failed to load health", error);
    return null;
  }
}

export async function getDiskUsage(): Promise<DiskUsage | null> {
  try {
    return await fetchJson<DiskUsage>("/system/disk-usage");
  } catch (error) {
    console.error("Failed to load disk usage", error);
    return null;
  }
}
