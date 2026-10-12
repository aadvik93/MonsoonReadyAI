import os
import shutil
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import httpx
except ImportError:
    httpx = None

from sqlmodel import create_engine, SQLModel

from .config import settings

# Database engine
engine = create_engine(settings.DATABASE_URL, echo=False)

# Initialize database tables
def init_db() -> None:
    """Create database tables if they do not exist."""
    SQLModel.metadata.create_all(engine)

# Call init on import so tables exist when app starts
init_db()

def compute_priority(report) -> Dict[str, Any]:
    """Deterministic priority scoring based on severity, water depth, and critical infrastructure.
    Returns a dict with 'score', 'category', and 'explanation'."""
    severity_weight = report.severity * 2.0
    depth_weight = (report.water_depth_cm or 0) * 0.1
    infra_weight = 5.0 if report.critical_infra else 0.0
    score = severity_weight + depth_weight + infra_weight
    if score >= 15:
        category = "HIGH"
    elif score >= 8:
        category = "MEDIUM"
    else:
        category = "LOW"
    explanation = (
        f"Severity ({report.severity}) contributes {severity_weight}, "
        f"water depth ({report.water_depth_cm or 0} cm) contributes {depth_weight:.1f}, "
        f"critical infra ({report.critical_infra}) contributes {infra_weight}. "
        f"Total score {score:.1f} => {category} priority."
    )
    return {"score": score, "category": category, "explanation": explanation}

def upload_to_s3(local_path: str, filename: str) -> str:
    """Upload a file to S3 or local fallback.
    Returns the storage key (S3 key or local filename)."""
    if settings.LOCAL_DEMO:
        dest_dir = Path(settings.LOCAL_UPLOAD_DIR)
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / filename
        shutil.copy(local_path, dest_path)
        return str(dest_path)
    # Real S3 upload (requires boto3 and credentials)
    try:
        import boto3
        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_DEFAULT_REGION,
        )
        bucket = settings.AWS_S3_BUCKET
        if not bucket:
            raise RuntimeError("AWS_S3_BUCKET not configured")
        s3.upload_file(local_path, bucket, filename)
        return f"{bucket}/{filename}"
    except Exception as e:
        if settings.LOCAL_DEMO:
            dest_dir = Path(settings.LOCAL_UPLOAD_DIR)
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_path = dest_dir / filename
            shutil.copy(local_path, dest_path)
            return str(dest_path)
        raise e

def generate_presigned_url(key: str) -> str:
    """Generate a presigned URL for a stored photo.
    In LOCAL_DEMO returns a file URI; otherwise uses S3 boto3."""
    if settings.LOCAL_DEMO:
        return f"file://{Path(key).absolute()}"
    try:
        import boto3
        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_DEFAULT_REGION,
        )
        bucket = settings.AWS_S3_BUCKET
        if not bucket:
            raise RuntimeError("AWS_S3_BUCKET not configured")
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=3600,
        )
        return url
    except Exception as e:
        if settings.LOCAL_DEMO:
            return f"file://{Path(key).absolute()}"
        raise e

def fetch_weather(latitude: float, longitude: float) -> Dict[str, Any]:
    """Fetch current weather from Open-Meteo API.
    Returns parsed JSON or empty dict on failure."""
    if httpx is None:
        return {}
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}&current_weather=true"
    )
    try:
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(url)
            resp.raise_for_status()
            data = resp.json()
            return data.get("current_weather", {})
    except Exception:
        return {}
