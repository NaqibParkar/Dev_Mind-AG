from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import get_settings
from .db.session import SessionLocal
from .routers import activity, auth, projects, settings, uploads


@asynccontextmanager
async def lifespan(_: FastAPI):
    db = SessionLocal()
    try:
        from . import crud

        crud.get_settings(db)
    finally:
        db.close()

    activity.tracker.start()
    yield
    activity.tracker.stop()


app = FastAPI(
    title="DevMind Backend",
    description="Cognitive Load & Activity Monitoring API",
    lifespan=lifespan,
)

configuration = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(configuration.cors_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(activity.router)
app.include_router(projects.router)
app.include_router(settings.router)
app.include_router(uploads.router)


@app.get("/", tags=["health"])
def read_root():
    return {"status": "Online", "message": "DevMind Backend is running"}


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy"}
