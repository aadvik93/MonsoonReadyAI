from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .router import api_router
from .config import settings

app = FastAPI(title="MonsoonReady AI Backend", version="0.1.0")

# CORS for dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/health")
async def health_check():
    if settings.LOCAL_DEMO:
        status = "LOCAL_DEMO"
    elif settings.AWS_S3_BUCKET:
        status = "CONNECTED"
    else:
        status = "NOT_CONFIGURED"
    return {"status": status}
