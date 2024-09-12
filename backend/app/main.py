from app.api.main import api_router
from app.core.config import settings
from app.pre_start import main
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="premstats", description="Service to query any English Premier League stat."
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# === ENDPOINTS ===


# Health Check
@app.get("/check")
async def healthcheck():
    return {"message": "Thus spoke St. Alia-of-the-Knife"}


# API
app.include_router(api_router, prefix="/api")
