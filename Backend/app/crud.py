from sqlalchemy.orm import Session
from . import models, schemas
import uuid
from typing import Optional

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_projects(db: Session):
    return db.query(models.Project).all()

def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(
        id=project.id,
        name=project.name,
        description=project.description,
        color=project.color,
        status=project.status
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project_status(db: Session, project_id: str, status: str):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project:
        project.status = status
        db.commit()
        db.refresh(project)
    return project

def delete_project(db: Session, project_id: str):
    # Delete associated activity logs first (Manual Cascade)
    db.query(models.ActivityLog).filter(models.ActivityLog.project_id == project_id).delete()
    
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project:
        db.delete(project)
        db.commit()
    return project

def get_settings(db: Session):
    settings = db.query(models.Settings).first()
    if not settings:
        # Create default
        settings = models.Settings()
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings

def update_settings(db: Session, settings: schemas.AppSettingsBase):
    db_settings = db.query(models.Settings).first()
    if not db_settings:
        db_settings = models.Settings()
        db.add(db_settings)
    
    db_settings.smart_breaks = settings.smartBreaks
    db_settings.comparative_mode = settings.comparativeMode
    db_settings.reflection_journal = settings.reflectionJournal
    db_settings.passive_mode = settings.passiveMode
    
    # Store alerts config flat for now (simplification)
    db_settings.alert_sensitivity = settings.alerts.sensitivity
    db_settings.alert_burnout = settings.alerts.types.get('burnout', True)
    db_settings.alert_focus_drop = settings.alerts.types.get('focusDrop', True)
    db_settings.alert_context_switching = settings.alerts.types.get('contextSwitching', True)
    db_settings.alert_prolonged_work = settings.alerts.types.get('prolongedWork', True)
    
    db.commit()
    db.refresh(db_settings)
    return db_settings

def log_activity(db: Session, activity: schemas.ActivityData):
    db_activity = models.ActivityLog(
        timestamp=activity.timestamp,
        keystrokes=activity.keystrokes,
        mouse_distance=activity.mouse_distance,
        active_window=activity.active_window,
        project_id=activity.project_id
    )
    # Here we would calculate focus score based on logic
    # For now, simplistic calculation
    # e.g. more keystrokes = higher focus up to a point
    
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def get_dashboard_stats(db: Session):
    # Calculate aggregates for "Today"
    # In a real app, filtering by date is essential.
    # For now, we take the latest log or average of recent logs.
    
    total_logs = db.query(models.ActivityLog).count()
    if total_logs == 0:
        return {
            "current_zone": "No Data",
            "focus_score": 0,
            "burnout_risk": "Low",
            "deep_work_minutes": 0,
            "chart_data": []
        }
    
    # Simple aggregation logic
    # Get logs from last 24h or just all for this MVP
    logs = db.query(models.ActivityLog).order_by(models.ActivityLog.timestamp.asc()).all()
    
    avg_focus = sum(l.focus_score for l in logs) / total_logs
    
    # Chart data: Group by hour?
    # Simplified: Just take the last 12 points or so
    chart_data = []
    for log in logs[-12:]:
        chart_data.append({
            "name": log.timestamp.strftime("%H:%M"),
            "val": log.cognitive_load
        })
        
    return {
        "current_zone": "Optimal Focus" if avg_focus > 70 else "Distracted",
        "focus_score": int(avg_focus),
        "burnout_risk": "Low", # logic pending
        "deep_work_minutes": 0, # logic pending
        "chart_data": chart_data
    }

def get_analytics_data(db: Session, project_id: Optional[str] = None, granularity: str = 'hourly'):
    query = db.query(models.ActivityLog)
    if project_id:
        query = query.filter(models.ActivityLog.project_id == project_id)
        
    logs = query.order_by(models.ActivityLog.timestamp.asc()).all()
    
    # Very simple aggregation for MVP
    # In a real app, this needs complex SQL time-bucketing
    data = []
    
    # Group by hour/day based on granularity
    # For now, just return raw logs mapped to chart format
    # Limit to reasonable amount to avoid UI crash
    limit = 24 if granularity == 'hourly' else 7
    
    for log in logs[-limit:]:
        data.append({
            "label": log.timestamp.strftime("%H:%M" if granularity == 'hourly' else "%a"),
            "focus": log.focus_score,
            "workload": int(log.cognitive_load * 100) if log.cognitive_load <= 1 else int(log.cognitive_load), # Normailze if needed
            "cognitiveLoad": int(log.cognitive_load * 100) if log.cognitive_load <= 1 else int(log.cognitive_load),
             # Comparative data (mocking 0 for now as we have no history)
            "prevFocus": 0,
            "prevWorkload": 0
        })
        
    return data
