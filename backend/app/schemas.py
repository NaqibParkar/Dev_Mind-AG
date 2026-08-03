from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# --- Pydantic Models for Input/Output ---

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    full_name: str | None = None

class User(UserBase):
    id: int
    full_name: str | None = None
    model_config = ConfigDict(from_attributes=True)

class ProjectBase(BaseModel):
    name: str
    description: str | None = None
    # color: str # Removed
    status: Literal['Active', 'Archived', 'Inactive'] = 'Active'

class ProjectCreate(ProjectBase):
    id: str # Allow client to generate ID or generate on backend. Let's accept ID from client for easy syncing.

class Project(ProjectBase):
    id: str
    timeSpentMinutes: int = 0
    avgFocusScore: int = 0
    workload: int = 0
    
    model_config = ConfigDict(from_attributes=True)

class AlertConfig(BaseModel):
    enabled: bool = True
    sensitivity: str = "Medium" # Relaxed from Literal to avoid strict issues
    types: dict = Field(default_factory=dict)

class AppSettingsBase(BaseModel):
    smartBreaks: bool
    comparativeMode: bool
    reflectionJournal: bool
    passiveMode: bool
    alerts: AlertConfig

class AppSettings(AppSettingsBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class Insight(BaseModel):
    id: str
    type: str
    title: str
    description: str

class CognitiveState(BaseModel):
    currentZone: str
    focusScore: int
    burnoutRisk: str
    focusStability: int
    deepWorkMinutes: int

# Activity Log Schema for receiving data from tracker
class ActivityData(BaseModel):
    timestamp: datetime
    keystrokes: int
    mouse_distance: float
    active_window: str | None = None
    project_id: str | None = None
