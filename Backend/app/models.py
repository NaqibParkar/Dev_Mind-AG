from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True) # Using UUID string to match frontend
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    color = Column(String)
    status = Column(String, default="Active") # Active, Archived, Inactive
    
    # Computed fields will need to be aggregated from ActivityLog
    
class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Metrics
    keystrokes = Column(Integer, default=0)
    mouse_distance = Column(Float, default=0.0)
    active_window = Column(String, nullable=True)
    
    # Derived Metrics (stored for easier querying)
    focus_score = Column(Integer, default=0)
    workload_score = Column(Integer, default=0)
    cognitive_load = Column(Integer, default=0)
    mental_state = Column(String, nullable=True)
    
class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(String, primary_key=True, index=True)
    date = Column(String, index=True) # ISO Date string YYYY-MM-DD
    emoji = Column(String)
    note = Column(String, nullable=True)
    
class Settings(Base):
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, default=1) # Single row for local app
    smart_breaks = Column(Boolean, default=True)
    comparative_mode = Column(Boolean, default=True)
    reflection_journal = Column(Boolean, default=True)
    passive_mode = Column(Boolean, default=False)
    
    # Alert Config (stored as JSON or separate columns, simple columns for now)
    alert_burnout = Column(Boolean, default=True)
    alert_focus_drop = Column(Boolean, default=True)
    alert_context_switching = Column(Boolean, default=True)
    alert_prolonged_work = Column(Boolean, default=True)
    alert_sensitivity = Column(String, default="Medium")
