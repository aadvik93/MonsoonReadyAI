// src/components/IncidentMap.tsx
import React from "react";
import { Report } from "../types";

interface Props {
  reports: Report[];
  width?: number;
  height?: number;
}

// Simple equirectangular projection for demo purposes
const toPx = (lat: number, lng: number, w: number, h: number) => {
  const x = ((lng + 180) / 360) * w;
  const y = ((90 - lat) / 180) * h;
  return { x, y };
};

export const IncidentMap: React.FC<Props> = ({ reports, width = 300, height = 150 }) => (
  <svg viewBox={`0 0 ${width} ${height}`} className="border rounded w-full max-w-md">
    {/* Ocean background */}
    <rect width={width} height={height} fill="#e0f7ff" />
    {/* Plot each incident */}
    {reports.map((r) => {
      const { x, y } = toPx(r.latitude, r.longitude, width, height);
      const color =
        r.priority_category === "HIGH"
          ? "#ef4444"
          : r.priority_category === "MEDIUM"
          ? "#f59e0b"
          : "#10b981";
      return (
        <circle
          key={r.report_id}
          cx={x}
          cy={y}
          r={4}
          fill={color}
          stroke="#fff"
          strokeWidth={1}
        />
      );
    })}
  </svg>
);

