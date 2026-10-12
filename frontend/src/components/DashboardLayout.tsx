// src/components/DashboardLayout.tsx
import React from "react";
import { NavLink } from "react-router-dom";

export const DashboardLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="flex h-screen bg-gray-50">
    {/* Sidebar */}
    <aside className="w-64 bg-white shadow-md flex flex-col p-4">
      <h2 className="text-xl font-semibold mb-6">MonsoonReady AI</h2>
      <nav className="space-y-2">
        <NavLink
          to="/dashboard"
          className={({ isActive }) =>
            `block py-2 px-3 rounded ${isActive ? "bg-indigo-100 text-indigo-700" : "text-gray-700"}`
          }
        >
          Dashboard
        </NavLink>
        <NavLink
          to="/report"
          className={({ isActive }) =>
            `block py-2 px-3 rounded ${isActive ? "bg-indigo-100 text-indigo-700" : "text-gray-700"}`
          }
        >
          New Report
        </NavLink>
      </nav>
    </aside>

    {/* Main area */}
    <main className="flex-1 overflow-auto">
      {/* Top bar */}
      <header className="flex justify-between items-center p-4 bg-white shadow">
        <h1 className="text-2xl font-semibold">Dashboard</h1>
        <span className="text-sm text-gray-500">Demo mode – local SQLite DB</span>
      </header>

      {/* Page content */}
      <section className="p-6">{children}</section>
    </main>
  </div>
);

