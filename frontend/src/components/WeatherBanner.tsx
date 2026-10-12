// src/components/WeatherBanner.tsx
import React, { useEffect, useState } from "react";
import { apiGet } from "../hooks/useApi";

export const WeatherBanner: React.FC = () => {
  const [weather, setWeather] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // Demo location – can be changed later
  const latitude = 28.6139; // Delhi lat (example)
  const longitude = 77.2090; // Delhi lon

  useEffect(() => {
    apiGet<any>(`/api/weather?latitude=${latitude}&longitude=${longitude}`)
      .then((data) => setWeather(data))
      .catch(() => setWeather({}))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return null;

  const isDemo = !weather || Object.keys(weather).length === 0;

  return (
    <div className="p-4 mb-4 rounded bg-blue-50 border border-blue-200">
      {isDemo ? (
        <p className="text-sm text-blue-800">Demo mode – no live weather data configured.</p>
      ) : (
        <p className="text-sm text-blue-800">
          Current temperature: {weather.temperature}°C, wind: {weather.windspeed} km/h
        </p>
      )}
    </div>
  );
};
