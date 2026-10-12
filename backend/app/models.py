from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Report(SQLModel, table=True):
    report_id: Optional[int] = Field(default=None, primary_key=True)
    location_name: str
    latitude: float
    longitude: float
    description: str
    severity: int  # 1-5 scale
    water_depth_cm: Optional[int] = None
    duration_minutes: Optional[int] = None
    critical_infra: Optional[bool] = None
    photo_key: Optional[str] = None  # S3 key or local filename
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="OPEN")  # OPEN, RESOLVED, CLOSED
    # priority fields populated by compute_priority
    priority_score: Optional[float] = None
    priority_category: Optional[str] = None
    priority_explanation: Optional[str] = None
