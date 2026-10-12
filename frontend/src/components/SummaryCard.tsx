// src/components/SummaryCard.tsx
import React from "react";

interface SummaryCardProps {
  title: string;
  value: number | string;
  color?: string; // Tailwind bg color class suffix, e.g., "blue-500"
}

const bgClassMap: Record<string, string> = {
  "blue-500": "bg-blue-500",
  "red-500": "bg-red-500",
  "green-500": "bg-green-500",
  "yellow-500": "bg-yellow-500",
};

const SummaryCard: React.FC<SummaryCardProps> = ({ title, value, color = "blue-500" }) => {
  const bgClass = bgClassMap[color] ?? "bg-blue-500";
  return (
    <div className={`p-4 rounded-lg shadow ${bgClass} text-white`}>
      <h3 className="text-sm font-medium">{title}</h3>
      <p className="text-2xl font-bold mt-1">{value}</p>
    </div>
  );
};

export default SummaryCard;
