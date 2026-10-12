// src/pages/Dashboard.tsx
import React, { useEffect, useState } from "react";
import { apiGet } from "../hooks/useApi";
import SummaryCard from "../components/SummaryCard";
import ReportCard from "../components/ReportCard";
import { Report } from "../types";
import { DashboardLayout } from "../components/DashboardLayout";
import { WeatherBanner } from "../components/WeatherBanner";
import { IncidentMap } from "../components/IncidentMap";

const Dashboard: React.FC = () => {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>("");
  const [priorityFilter, setPriorityFilter] = useState<string>("");
  const [search, setSearch] = useState<string>("");

  const fetchReports = async () => {
    try {
      setLoading(true);
      const data = await apiGet<Report[]>("/api/reports");
      setReports(data);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const filtered = reports.filter((r) => {
    const matchesStatus = statusFilter ? r.status === statusFilter : true;
    const matchesPriority = priorityFilter ? (r.priority_category || "LOW") === priorityFilter : true;
    const matchesSearch = search
      ? r.location_name.toLowerCase().includes(search.toLowerCase()) ||
        r.description.toLowerCase().includes(search.toLowerCase())
      : true;
    return matchesStatus && matchesPriority && matchesSearch;
  });

  const totalReports = reports.length;
  const highRisk = reports.filter((r) => r.priority_category === "HIGH").length;
  const openCount = reports.filter((r) => r.status === "OPEN").length;
  const resolvedCount = reports.filter((r) => r.status === "RESOLVED").length;

  if (loading) return <div className="p-4">Loading dashboard…</div>;
  if (error) return <div className="p-4 text-red-600">Error: {error}</div>;

  return (
    <DashboardLayout>
      <WeatherBanner />
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <SummaryCard title="Total Reports" value={totalReports} />
        <SummaryCard title="High‑Risk" value={highRisk} color="red-500" />
        <SummaryCard title="Open" value={openCount} color="yellow-500" />
        <SummaryCard title="Resolved" value={resolvedCount} color="green-500" />
      </div>

      <div className="flex flex-wrap gap-2 mb-4">
        <select className="border rounded p-1" value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
          <option value="">All Statuses</option>
          <option value="OPEN">OPEN</option>
          <option value="RESOLVED">RESOLVED</option>
          <option value="CLOSED">CLOSED</option>
        </select>
        <select className="border rounded p-1" value={priorityFilter} onChange={(e) => setPriorityFilter(e.target.value)}>
          <option value="">All Priorities</option>
          <option value="HIGH">HIGH</option>
          <option value="MEDIUM">MEDIUM</option>
          <option value="LOW">LOW</option>
        </select>
        <input
          type="text"
          placeholder="Search…"
          className="border rounded p-1 flex-1"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <a href="/report" className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700">
          New Report
        </a>
      </div>

      <IncidentMap reports={filtered} />

      {filtered.length === 0 ? (
        <div>No reports match the criteria.</div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {filtered.map((r) => (
            <ReportCard key={r.report_id} report={r} />
          ))}
        </div>
      )}
    </DashboardLayout>
  );
};

export default Dashboard;
