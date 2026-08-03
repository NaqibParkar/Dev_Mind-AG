from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud
from ..db import models
from ..db.session import get_db
from ..services.activity_tracker import ActivityTracker
from ..services.burnout_predictor import BurnoutPredictor

router = APIRouter(prefix="/activity", tags=["activity"])
tracker = ActivityTracker()
predictor = BurnoutPredictor()


@router.get("/live")
def get_live_activity(db: Session = Depends(get_db)):
    memory_stats = tracker.get_current_stats()
    latest = (
        db.query(models.ActivityLog)
        .order_by(models.ActivityLog.timestamp.desc())
        .first()
    )

    cognitive_load = latest.cognitive_load if latest else 0
    focus_score = latest.focus_score if latest else 0
    try:
        burnout_risk = predictor.predict(
            cognitive_load=cognitive_load,
            focus_score=focus_score,
            keystrokes=memory_stats.get("last_interval_keystrokes", 0) * 12,
            mouse_dist=memory_stats.get("last_interval_mouse", 0),
        )
    except Exception:
        burnout_risk = "Unknown"

    return {
        "keystrokes": memory_stats.get("keystrokes", 0),
        "mouse_intensity": int(memory_stats.get("mouse_distance", 0)),
        "focus_score": focus_score,
        "cognitive_load": cognitive_load,
        "active_window": memory_stats.get("active_window") or "Unknown",
        "burnout_risk": burnout_risk,
        "context_switches": memory_stats.get("context_switches", 0),
    }


@router.get("/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    return crud.get_dashboard_stats(db)


@router.get("/analytics")
def get_analytics_data(
    project_id: str | None = None,
    granularity: str = "hourly",
    db: Session = Depends(get_db),
):
    return crud.get_analytics_data(db, project_id, granularity)

