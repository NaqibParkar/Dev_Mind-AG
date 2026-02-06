from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

# Local imports - adjusted for your app/ folder structure
from . import crud, models, schemas
from .database import SessionLocal, engine, get_db
from .tracker import ActivityTracker

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
    
    return {
        "keystrokes": memory_stats.get("keystrokes", 0),
        "mouse_intensity": memory_stats.get("mouse_distance", 0),
        "focus_score": latest.focus_score if latest else 0,
        "cognitive_load": latest.cognitive_load if latest else 0,
        "active_window": latest.active_window if latest else "Initializing..."
    }

# --- Project Management Routes ---
@app.get("/projects", response_model=list[schemas.Project])
def read_projects(db: Session = Depends(get_db)):
    projects = crud.get_projects(db)
    results = []
    for p in projects:
        # Transforming DB model to match your frontend types.ts requirements
        results.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "color": p.color,
            "status": p.status,
            "timeSpentMinutes": 120, # In a final version, calculate this from ActivityLog
            "avgFocusScore": 75,
            "workload": 50
        })
    return results

@app.post("/projects", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)

@app.put("/projects/{project_id}/status")
def update_project_status(project_id: str, status: str, db: Session = Depends(get_db)):
    updated_project = crud.update_project_status(db=db, project_id=project_id, status=status)
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project

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