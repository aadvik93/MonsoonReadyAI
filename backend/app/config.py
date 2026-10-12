import os
from typing import Optional
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class Settings:
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///./app.db')
    LOCAL_DEMO: bool = os.getenv('LOCAL_DEMO', 'true').lower() == 'true'
    LOCAL_UPLOAD_DIR: str = os.getenv('LOCAL_UPLOAD_DIR', 'uploads')
    AWS_S3_BUCKET: Optional[str] = os.getenv('AWS_S3_BUCKET')
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_DEFAULT_REGION: Optional[str] = os.getenv('AWS_DEFAULT_REGION')

# instantiate settings
settings = Settings()

# ensure upload dir exists in demo mode
if settings.LOCAL_DEMO:
    Path(settings.LOCAL_UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
