// src/hooks/useApi.ts
const API_BASE = "http://localhost:8000"; // FastAPI dev server

export async function apiGet<T>(path: string): Promise<T> {
  const resp = await fetch(`${API_BASE}${path}`);
  if (!resp.ok) {
    const err = await resp.text();
    throw new Error(`GET ${path} failed: ${resp.status} ${err}`);
  }
  return resp.json();
}

export async function apiPost<T>(path: string, body: any, isFormData = false): Promise<T> {
  const resp = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: isFormData ? undefined : { "Content-Type": "application/json" },
    body: isFormData ? body : JSON.stringify(body),
  });
  if (!resp.ok) {
    const err = await resp.text();
    throw new Error(`POST ${path} failed: ${resp.status} ${err}`);
  }
  return resp.json();
}

export async function apiPatch<T>(path: string, body: any): Promise<T> {
  const resp = await fetch(`${API_BASE}${path}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!resp.ok) {
    const err = await resp.text();
    throw new Error(`PATCH ${path} failed: ${resp.status} ${err}`);
  }
  return resp.json();
}
