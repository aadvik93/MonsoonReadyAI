# MonsoonReady AI

## Project Purpose
MonsoonReady AI is a real‑time water‑logging incident reporting and risk‑prioritization platform designed for the **WeMakeDevs × AWS Environmental Hacks 2026** hackathon (Heat and Water track). It enables citizens, NGOs, and municipal operators to quickly submit water‑logging events, automatically calculates a deterministic risk score, provides actionable safety recommendations, and enriches reports with live weather context.

## Features
- **Incident Dashboard** – summary cards, searchable/filterable incident list.
- **Report Form** – location, severity, water depth, duration, optional photo upload.
- **Risk Scoring** – deterministic algorithm with explainable factors and priority categories (`HIGH`, `MEDIUM`, `LOW`).
- **Weather Integration** – fetches current weather from Open‑Meteo (fallback to empty when unavailable).
- **Photo Storage** – stores photos locally in demo mode or uploads to a private Amazon S3 bucket when configured.
- **SQLite Persistence** – all incident data stored in a local SQLite database (`app.db`).
- **Responsive UI** – built with React, Vite, TypeScript, and Tailwind CSS.
- **Local Demo Mode** – works without any AWS credentials; clearly indicates demo status.

## Tech Stack
- **Frontend** – React 18, Vite, TypeScript, Tailwind CSS, React Router v6.
- **Backend** – FastAPI, Uvicorn, SQLModel (SQLite), httpx (weather), boto3 (S3).
- **Database** – SQLite (`sqlite:///./app.db`).
- **Deployment** – Designed for local Docker or simple Python execution; optional AWS integration for photo storage.

---

---

## 🛠️ AWS SAM Lambda – Local Risk Scoring

MonsoonReady AI now includes a minimal **AWS SAM**‑based Lambda that implements the same risk‑scoring algorithm used by the FastAPI backend. The Lambda runs **locally** with the SAM CLI (no AWS account, no charges).

### Files added
- `aws_lambda/priority/app.py` – Lambda handler (`lambda_handler`) and pure‑Python `compute_priority`.
- `aws_lambda/priority/template.yaml` – SAM template that declares `PriorityFunction`.
- `aws_lambda/priority/sample-event.json` – Example payload for testing.
- `aws_lambda/priority/test_compare.py` – Python script that runs the backend and Lambda implementations on the same data and asserts equality.

### Running the comparison test (no Docker needed)
```bash
# From the project root
python aws_lambda/priority/test_compare.py
```
You should see:
```
✅ Lambda output matches backend compute_priority
```
The script exits with status 0, confirming the Lambda logic matches the existing backend.

### (Optional) Full SAM local execution – requires Docker
If Docker is available you can also build and invoke the Lambda with SAM:
```bash
# Install SAM CLI (once)
brew install aws-sam-cli
# Build the function
sam build -t aws_lambda/priority/template.yaml
# Invoke with the sample event
sam local invoke PriorityFunction --event aws_lambda/priority/sample-event.json
```
The output will be the same JSON payload as the test script.

### Why this satisfies the hackathon requirement
The **AWS SAM CLI** is an official open‑source tool listed on the WeMakeDevs × AWS Environmental Hacks 2026 page. By creating a Lambda function and invoking it locally with SAM we demonstrate the use of an AWS development workflow **without deploying any cloud resources or incurring costs**. The Lambda uses only standard Python libraries, keeping the solution fully offline.

---
