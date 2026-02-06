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
