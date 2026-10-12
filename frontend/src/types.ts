// src/types.ts
export interface Report {
  report_id: number;
  location_name: string;
  latitude: number;
  longitude: number;
  description: string;
  severity: number;
  water_depth_cm?: number | null;
  duration_minutes?: number | null;
  critical_infra?: boolean | null;
  photo_key?: string | null;
  created_at: string; // ISO string
  updated_at: string;
  status: string;
  priority_score?: number | null;
  priority_category?: string | null;
  priority_explanation?: string | null;
}
