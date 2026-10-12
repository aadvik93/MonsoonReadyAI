// src/App.tsx
import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import ReportForm from "./pages/ReportForm";
import IncidentDetail from "./pages/IncidentDetail";

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/report" element={<ReportForm />} />
        <Route path="/incident/:id" element={<IncidentDetail />} />
        <Route path="*" element={<div className="p-4 text-center">Page not found</div>} />
      </Routes>
    </div>
  );
};

export default App;
