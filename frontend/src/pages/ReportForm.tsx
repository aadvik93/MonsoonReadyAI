// src/pages/ReportForm.tsx
import React, { useState } from "react";
import { apiPost } from "../hooks/useApi";
import { useNavigate } from "react-router-dom";

const ReportForm: React.FC = () => {
  const navigate = useNavigate();
  const [formState, setFormState] = useState({
    location_name: "",
    latitude: "",
    longitude: "",
    description: "",
    severity: "1",
    water_depth_cm: "",
    duration_minutes: "",
    critical_infra: false,
    photo: null as File | null,
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<boolean>(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type, checked, files } = e.target as any;
    if (type === "file") {
      setFormState({ ...formState, [name]: files[0] });
    } else if (type === "checkbox") {
      setFormState({ ...formState, [name]: checked });
    } else {
      setFormState({ ...formState, [name]: value });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Basic validation
    const isNumber = (v: string) => !isNaN(Number(v));
    if (
      !formState.location_name ||
      !formState.description ||
      !formState.latitude ||
      !formState.longitude ||
      !formState.severity ||
      !isNumber(formState.latitude) ||
      !isNumber(formState.longitude) ||
      !isNumber(formState.severity)
    ) {
      setError("Please fill out all required fields with valid numbers.");
      return;
    }
    setSubmitting(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append("location_name", formState.location_name);
      formData.append("latitude", formState.latitude);
      formData.append("longitude", formState.longitude);
      formData.append("description", formState.description);
      formData.append("severity", formState.severity);
      if (formState.water_depth_cm) formData.append("water_depth_cm", formState.water_depth_cm);
      if (formState.duration_minutes) formData.append("duration_minutes", formState.duration_minutes);
      if (formState.critical_infra) formData.append("critical_infra", "true");
      if (formState.photo) formData.append("photo", formState.photo);

      await apiPost("/api/reports", formData, true);
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
      navigate("/dashboard");
    } catch (e: any) {
      setError(e.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto p-4">
      <h2 className="text-xl font-bold mb-4">New Waterlogging Report</h2>
      {error && <div className="text-red-600 mb-2">Error: {error}</div>}
      {success && <div className="text-green-600 mb-2">Report submitted successfully!</div>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          required
          name="location_name"
          placeholder="Location name"
          className="w-full border p-2 rounded"
          value={formState.location_name}
          onChange={handleChange}
        />
        <div className="flex space-x-2">
          <input
            required
            name="latitude"
            placeholder="Latitude"
            className="flex-1 border p-2 rounded"
            value={formState.latitude}
            onChange={handleChange}
          />
          <input
            required
            name="longitude"
            placeholder="Longitude"
            className="flex-1 border p-2 rounded"
            value={formState.longitude}
            onChange={handleChange}
          />
        </div>
        <textarea
          required
          name="description"
          placeholder="Description"
          className="w-full border p-2 rounded"
          rows={3}
          value={formState.description}
          onChange={handleChange}
        />
        <select
          name="severity"
          className="w-full border p-2 rounded"
          value={formState.severity}
          onChange={handleChange}
        >
          {[1, 2, 3, 4, 5].map((v) => (
            <option key={v} value={v.toString()}>{v}</option>
          ))}
        </select>
        <input
          name="water_depth_cm"
          placeholder="Water depth (cm)"
          className="w-full border p-2 rounded"
          type="number"
          value={formState.water_depth_cm}
          onChange={handleChange}
        />
        <input
          name="duration_minutes"
          placeholder="Duration (minutes)"
          className="w-full border p-2 rounded"
          type="number"
          value={formState.duration_minutes}
          onChange={handleChange}
        />
        <label className="flex items-center space-x-2">
          <input
            type="checkbox"
            name="critical_infra"
            checked={formState.critical_infra}
            onChange={handleChange}
          />
          <span>Critical infrastructure affected</span>
        </label>
        <input
          type="file"
          name="photo"
          accept="image/*"
          onChange={handleChange}
        />
        <button
          type="submit"
          disabled={submitting}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          {submitting ? "Submitting…" : "Submit Report"}
        </button>
      </form>
    </div>
  );
};

export default ReportForm;
