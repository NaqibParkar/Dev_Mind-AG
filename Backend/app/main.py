from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

# Local imports - adjusted for your app/ folder structure
from . import crud, models, schemas
from .database import SessionLocal, engine, get_db
from .tracker import ActivityTracker
from .routers import auth

# 1. Initialize Database Tables
# This ensures devmind.db has the latest ActivityLog schema
models.Base.metadata.create_all(bind=engine)

# 2. Global Tracker Instance
tracker = ActivityTracker()

# 3. Lifespan Context Manager
# This starts/stops the pynput listeners when the server starts/stops
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start hardware listeners (keyboard and mouse)
    tracker.start()
    
    # Database Clean-up: Ensure Settings exist
    db = SessionLocal()
    try:
        if not crud.get_settings(db):
            print("Initializing default settings...")
    except Exception as e:
        print(f"Error initializing settings: {e}")
    finally:
        db.close()

    yield
    # Shutdown: Stop hardware listeners safely
    tracker.stop()

# 4. FastAPI Application Initialization
app = FastAPI(
    title="DevMind Backend",
    description="Cognitive Load & Activity Monitoring API",
    lifespan=lifespan
)

app.include_router(auth.router)

# 5. CORS Configuration
# Allows your Vite/React frontend to communicate with this API
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"status": "Online", "message": "DevMind Backend is running"}

@app.get("/activity/live")
def get_live_activity(db: Session = Depends(get_db)):
    # Get un-saved raw numbers directly from tracker memory
    memory_stats = tracker.get_current_stats()
    
    # Get the latest processed record from SQLite
    latest = db.query(models.ActivityLog).order_by(models.ActivityLog.timestamp.desc()).first()
    
    # ML Prediction for Burnout Risk
    # current_keystrokes is instantaneous from memory, but model trained on rate/min?
    # Let's scale it slightly or just pass raw. Synthetic model expects 0-500 rate.
    # memory stats are likely small (since last clear 5s ago).
    # so we project to minute rate: val * 12
    
    # ML Prediction for Burnout Risk
    burnout_risk = "Low" # Default
    try:
        kpm = memory_stats.get("keystrokes", 0) * 12 
        mouse_activity = memory_stats.get("mouse_distance", 0)
        
        cog_load = latest.cognitive_load if latest else 0
        focus = latest.focus_score if latest else 0
        
        burnout_risk = predictor.predict(
            cognitive_load=cog_load,
            focus_score=focus,
            keystrokes=kpm,
            mouse_dist=mouse_activity
        )
    except Exception as e:
        print(f"ML Prediction Warning: {e}")
        burnout_risk = "Error"

    # Active Window Logic
    # Strict Real-time: Do NOT fallback to DB for "Active Window". 
    # DB is history. This is live.
    live_window = memory_stats.get("active_window")
    if not live_window:
        live_window = "Unknown"
        
    return {
        "keystrokes": memory_stats.get("keystrokes", 0),
        "mouse_intensity": memory_stats.get("mouse_distance", 0),
        "focus_score": focus,
        "cognitive_load": cog_load,
        "active_window": live_window,
        "burnout_risk": burnout_risk 
    }

@app.get("/activity/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Returns aggregated stats for the main dashboard.
    """
    return crud.get_dashboard_stats(db)

@app.get("/activity/analytics")
def get_analytics_data(project_id: str = None, granularity: str = 'hourly', db: Session = Depends(get_db)):
    """
    Returns historical analytics data.
    """
    return crud.get_analytics_data(db, project_id, granularity)

# --- Project Management Routes ---
@app.get("/projects", response_model=list[schemas.Project])
def read_projects(db: Session = Depends(get_db)):
    projects = crud.get_projects(db)
    return projects

@app.post("/projects", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)

@app.put("/projects/{project_id}/status")
def update_project_status(project_id: str, status: str, db: Session = Depends(get_db)):
    updated_project = crud.update_project_status(db=db, project_id=project_id, status=status)
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project

@app.delete("/projects/{project_id}")
def delete_project(project_id: str, db: Session = Depends(get_db)):
    deleted_project = crud.delete_project(db=db, project_id=project_id)
    if not deleted_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully", "id": project_id}

# --- Settings & Configuration ---
@app.get("/settings", response_model=schemas.AppSettings)
def read_settings(db: Session = Depends(get_db)):
    settings_db = crud.get_settings(db)
    if not settings_db:
        raise HTTPException(status_code=404, detail="Settings not found")
        
    return {
        "id": settings_db.id,
        "smartBreaks": settings_db.smart_breaks,
        "comparativeMode": settings_db.comparative_mode,
        "reflectionJournal": settings_db.reflection_journal,
        "passiveMode": settings_db.passive_mode,
        "alerts": {
            "enabled": True,
            "sensitivity": settings_db.alert_sensitivity,
            "types": {
                "burnout": settings_db.alert_burnout,
                "focusDrop": settings_db.alert_focus_drop,
                "contextSwitching": settings_db.alert_context_switching,
                "prolongedWork": settings_db.alert_prolonged_work
            }
        }
    }

@app.put("/settings", response_model=schemas.AppSettings)
def update_settings(settings: schemas.AppSettingsBase, db: Session = Depends(get_db)):
    return crud.update_settings(db=db, settings=settings)