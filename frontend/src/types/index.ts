export interface Shoot {
  id: string;
  name: string;
  location?: string;
  captured_at: string;
  tags: string[];
}

export interface Photo {
  id: string;
  shoot_id: string;
  filename: string;
  captured_at: string;
  rating?: number;
  labels: string[];
  preview_path?: string;
}

export interface Timelapse {
  id: string;
  title: string;
  shoot_ids: string[];
  frame_count: number;
  video_path?: string;
}

export interface JobStatus {
  id: string;
  name: string;
  status: string;
  created_at: string;
  updated_at: string;
  log_path?: string;
}

export interface HealthStatus {
  status: string;
}

export interface DiskUsage {
  root: string;
  used_gb: number;
  free_gb: number;
}
