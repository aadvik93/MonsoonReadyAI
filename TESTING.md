# MonsoonReady AI - Testing Guide

## Backend tests
- **Framework**: pytest
- **Location**: `backend/tests/`
- Install dependencies: `pip install -r requirements.txt pytest httpx`
- Run: `pytest backend/tests/`

### Test cases (to be implemented)
1. **Health endpoint** – GET `/health` returns status field.
2. **Create report** – POST `/api/reports` with valid multipart data creates a report and returns all fields including priority.
3. **List reports** – GET `/api/reports` returns list; supports query filters.
4. **Get single report** – GET `/api/reports/{id}` returns correct report or 404.
5. **Update status** – PATCH `/api/reports/{id}?status=RESOLVED` updates `status`.
6. **Weather fallback** – GET `/api/weather` with unreachable Open‑Meteo returns empty dict.
7. **Presigned URL** – GET `/api/presigned/{id}` returns a URL when photo exists, 404 otherwise.
8. **Invalid data** – POST with missing required fields returns 422.

## Frontend tests
- **Framework**: Vitest (included with Vite)
- **Location**: `frontend/tests/`
- Run: `npm run test` (or `npx vitest`)

### Test scenarios (to be added)
1. **Dashboard renders summary cards** – verifies totals based on mocked API response.
2. **Report form validation** – required fields block submission.
3. **Incident detail status update** – clicking "Mark Resolved" sends a PATCH request and UI updates.
4. **Error handling** – displays error message on API failure.
5. **Loading states** – shows loading indicator while fetching data.

> The tests are provided as skeleton files; you can fill in implementation details.
