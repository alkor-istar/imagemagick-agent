from fastapi import FastAPI
from app.api.routes import router
from app.config import load_settings
from app.services.imagick_agent import build_imagick_agent
from fastapi.middleware.cors import CORSMiddleware
import os


def create_app() -> FastAPI:
    settings = load_settings()

    app = FastAPI(title="ImageMagick LLM Agent", version="0.1.0")
    print("CORS", settings.cors_origins)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["POST", "GET", "OPTIONS"],
        allow_headers=["*"],
    )

    app.state.agent = build_imagick_agent(settings)

    app.include_router(router)

    return app


app = create_app()
