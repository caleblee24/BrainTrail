from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .db import Base, engine
from .models import *  # noqa
from .services import embeddings
from .routers import auth, goals, resources, progress, tutor
import os

def create_app() -> FastAPI:
    app = FastAPI(title="AI Knowledge Hub API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[o.strip() for o in settings.CORS_ORIGINS.split(',')],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def on_startup():
        if os.getenv("RUN_CREATE_ALL", "true").lower() == "true":
            Base.metadata.create_all(bind=engine)
        embeddings.startup()

    app.include_router(auth.router)
    app.include_router(goals.router)
    app.include_router(resources.router)
    app.include_router(progress.router)
    app.include_router(tutor.router)
    return app
