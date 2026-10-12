// src/pages/IncidentDetail.tsx
import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { apiGet, apiPatch } from "../hooks/useApi";
import { Report } from "../types";

const IncidentDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [report, setReport] = useState<Report | null>(null);
  const [weather, setWeather] = useState<any>(null);
  const [photoUrl, setPhotoUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [updating, setUpdating] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      const r = await apiGet<Report>(`/api/reports/${id}`);
      setReport(r);
      // fetch weather based on location
      const w = await apiGet<any>(`/api/weather?latitude=${r.latitude}&longitude=${r.longitude}`);
      setWeather(w);
      // fetch photo URL if exists
      if (r.photo_key) {
        const p = await apiGet<{ url: string }>(`/api/presigned/${id}`);
        setPhotoUrl(p.url);
      }
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const handleStatusChange = async (newStatus: string) => {
    if (!report) return;
    try {
      setUpdating(true);
      await apiPatch<Report>(`/api/reports/${report.report_id}?status=${newStatus}`, {});
      // re-fetch to refresh UI
      await fetchData();
    } catch (e: any) {
      setError(e.message);
    } finally {
      setUpdating(false);
    }
  };

  if (loading) return <div className="p-4">Loading incident…</div>;
  if (error) return <div className="p-4 text-red-600">Error: {error}</div>;
  if (!report) return <div className="p-4">Incident not found.</div>;

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <button onClick={() => navigate(-1)} className="text-blue-600 mb-4">← Back</button>
      <h2 className="text-2xl font-bold mb-2">{report.location_name}</h2>
      <p className="mb-1"><strong>Description:</strong> {report.description}</p>
      <p className="mb-1"><strong>Severity:</strong> {report.severity}</p>
      <p className="mb-1"><strong>Status:</strong> {report.status}</p>
      <p className="mb-1"><strong>Priority:</strong> {report.priority_category || "LOW"}</p>
      <p className="mb-1"><strong>Score:</strong> {report.priority_score?.toFixed(1) || "-"}</p>
      {weather && (
        <div className="mt-4 p-2 border rounded">
          <h3 className="font-semibold mb-1">Current Weather (Open‑Meteo)</h3>
          <pre className="text-sm">{JSON.stringify(weather, null, 2)}</pre>
        </div>
      )}
      {photoUrl && (
        <div className="mt-4">
          <h3 className="font-semibold mb-1">Photo</h3>
          <img src={photoUrl} alt="Incident photo" className="max-w-full h-auto" />
        </div>
      )}
      <div className="mt-6 flex space-x-2">
        <button
          onClick={() => handleStatusChange("RESOLVED")}
          disabled={updating || report.status === "RESOLVED"}
          className="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
        >
          Mark Resolved
        </button>
        <button
          onClick={() => handleStatusChange("CLOSED")}
          disabled={updating || report.status === "CLOSED"}
          className="bg-gray-600 text-white px-3 py-1 rounded hover:bg-gray-700"
        >
          Close
        </button>
      </div>
    </div>
  );
};

export default IncidentDetail;
