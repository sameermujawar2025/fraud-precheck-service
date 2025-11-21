# app/main.py
from fastapi import FastAPI
from app.api.feature_router import router as feature_router
from app.api.blacklist_router import router as blacklist_router
from app.config.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description="Feature service for real-time fraud detection (R1–R9)."
    )

    app.include_router(feature_router)
    app.include_router(blacklist_router)

    @app.get("/health")
    def health():
        return {"status": "UP"}

    return app


app = create_app()
