from fastapi import FastAPI
from app.api.routes import router
from app.config import load_settings
from app.services.imagick_agent import build_imagick_agent
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    settings = load_settings()

    app = FastAPI(title="ImageMagick LLM Agent", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://[::1]:5173",
            "http://127.0.0.1:5173",
        ],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.state.agent = build_imagick_agent(settings)

    app.include_router(router)

    return app


app = create_app()
