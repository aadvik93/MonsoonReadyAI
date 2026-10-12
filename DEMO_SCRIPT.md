# DEMO SCRIPT

**Goal:** Demonstrate the core workflow of MonsoonReady AI in ~3 minutes.

1. **Start backend**
   ```bash
   cd backend
   uvicorn app.main:app --reload --port 8000
   ```
   - Verify the health endpoint: `curl http://localhost:8000/health`.
   - The response should contain `"status": "LOCAL_DEMO"` (no AWS credentials).

2. **Start frontend**
   ```bash
   cd ../frontend
   npm install   # (already done in repository)
   npm run dev
   ```
   - Open the URL printed by Vite (typically http://localhost:5173).

3. **Dashboard overview**
   - The dashboard shows three summary cards (Total Reports, High‑Risk, Resolved).
   - In demo mode the data is empty; you will see a friendly *Demo data* badge.

4. **Create a new incident**
   - Click **Create Report** → fill the form:
     - Location: *Riverbank Park*
     - Latitude / Longitude: `12.34`, `56.78`
     - Description: *Water level rose after heavy rain.*
     - Severity: `4`
     - Water depth (cm): `30`
     - Duration (minutes): `45`
     - Critical Infrastructure: checked
     - Photo: optionally attach any image file.
   - Submit. The app shows a loading spinner, then navigates back to the dashboard.
   - The new report appears in the list with a **Risk Score** badge and a **Pending** status.

5. **Inspect incident detail**
   - Click the report card to open the detail page.
   - Verify:
     - All fields are displayed.
     - A **Risk Explanation** explains why the score is high.
     - Weather context shows *unavailable* (demo mode) with a helpful message.
     - If a photo was uploaded, a thumbnail preview loads via a local `file://` URL.

6. **Update status**
   - Click **Mark Resolved**. The app sends a PATCH request.
   - The status badge changes to **Resolved** and the dashboard summary updates.

7. **Show AWS fallback (optional)**
   - Edit the `.env` file to set `LOCAL_DEMO=false` and provide valid AWS credentials.
   - Restart the backend. The health endpoint now reports `"status": "AWS_READY"`.
   - Re‑create a report with a photo; the photo is uploaded to the configured S3 bucket and the detail page shows a presigned URL.

8. **Wrap‑up**
   - Summarize the impact: rapid incident reporting, deterministic scoring, and cloud‑ready photo storage.
   - Mention future extensions (real‑time sensor integration, automated alerts).

**Tips for judges:**
- Keep the demo concise; focus on the *report‑to‑resolution* flow.
- Highlight the fallback behavior when the weather API or AWS is unavailable.
- Emphasize the clean UI and the deterministic risk algorithm.
