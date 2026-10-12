from fastapi import APIRouter, Form, File, UploadFile, Query, HTTPException
from typing import List, Optional
from sqlmodel import Session, select
from .models import Report
from .utils import upload_to_s3, generate_presigned_url, fetch_weather, engine
from .risk import compute_priority

api_router = APIRouter()

@api_router.post("/reports", response_model=Report)
async def create_report(
    location_name: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    description: str = Form(...),
    severity: int = Form(...),
    water_depth_cm: Optional[int] = Form(None),
    duration_minutes: Optional[int] = Form(None),
    critical_infra: Optional[bool] = Form(None),
    photo: Optional[UploadFile] = File(None),
):
    # Build report object
    report = Report(
        location_name=location_name,
        latitude=latitude,
        longitude=longitude,
        description=description,
        severity=severity,
        water_depth_cm=water_depth_cm,
        duration_minutes=duration_minutes,
        critical_infra=critical_infra,
    )
    # Compute priority
    pr = compute_priority(report)
    report.priority_score = pr["score"]
    report.priority_category = pr["category"]
    report.priority_explanation = pr["explanation"]
    # Handle photo upload
    if photo:
        temp_path = f"/tmp/{photo.filename}"
        with open(temp_path, "wb") as f:
            content = await photo.read()
            f.write(content)
        key = upload_to_s3(temp_path, photo.filename)
        report.photo_key = key
    # Save to DB
    with Session(engine) as session:
        session.add(report)
        session.commit()
        session.refresh(report)
        return report

@api_router.get("/reports", response_model=List[Report])
def list_reports(
    status: Optional[str] = Query(None),
    priority_category: Optional[str] = Query(None),
    location_name: Optional[str] = Query(None),
):
    with Session(engine) as session:
        stmt = select(Report)
        if status:
            stmt = stmt.where(Report.status == status)
        if priority_category:
            stmt = stmt.where(Report.priority_category == priority_category)
        if location_name:
            stmt = stmt.where(Report.location_name.ilike(f"%{location_name}%"))
        results = session.exec(stmt).all()
        return results

@api_router.get("/reports/{report_id}", response_model=Report)
def get_report(report_id: int):
    with Session(engine) as session:
        report = session.get(Report, report_id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        return report

@api_router.patch("/reports/{report_id}", response_model=Report)
def update_report(
    report_id: int,
    status: Optional[str] = Query(None),
    resolution_note: Optional[str] = Query(None)
):
    with Session(engine) as session:
        report = session.get(Report, report_id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        if status:
            report.status = status
        # resolution_note could be stored in a separate field; omitted for brevity
        session.add(report)
        session.commit()
        session.refresh(report)
        return report

@api_router.get("/presigned/{report_id}")
def get_presigned_url(report_id: int):
    with Session(engine) as session:
        report = session.get(Report, report_id)
        if not report or not report.photo_key:
            raise HTTPException(status_code=404, detail="Photo not found")
        url = generate_presigned_url(report.photo_key)
        return {"url": url}

@api_router.get("/weather")
def get_weather(latitude: float = Query(...), longitude: float = Query(...)):
    weather = fetch_weather(latitude, longitude)
    return weather
