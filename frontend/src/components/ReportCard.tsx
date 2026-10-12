// src/components/ReportCard.tsx
import React from "react";
import { Link } from "react-router-dom";
import { Report } from "../types";

interface ReportCardProps {
  report: Report;
}

const priorityColor = (category: string) => {
  switch (category) {
    case "HIGH":
      return "bg-red-500";
    case "MEDIUM":
      return "bg-yellow-500";
    default:
      return "bg-green-500";
  }
};

const ReportCard: React.FC<ReportCardProps> = ({ report }) => {
  return (
    <div className="border rounded p-4 shadow hover:shadow-lg transition">
      <div className="flex justify-between items-start">
        <h3 className="text-lg font-semibold">{report.location_name}</h3>
        <span className={`text-sm text-white px-2 py-1 rounded ${priorityColor(report.priority_category || "LOW")}`}> 
          {report.priority_category || "LOW"}
        </span>
      </div>
      <p className="text-sm mt-1">Severity: {report.severity}</p>
      <p className="text-sm">Status: {report.status}</p>
      <p className="text-xs text-gray-500 mt-2">Created: {new Date(report.created_at).toLocaleString()}</p>
      <Link to={`/incident/${report.report_id}`} className="text-blue-600 mt-2 inline-block">View details →</Link>
    </div>
  );
};

export default ReportCard;
