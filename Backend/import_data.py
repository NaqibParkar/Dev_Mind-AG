import csv
import os
import sys
from datetime import datetime

# Add app to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database import SessionLocal, engine
from app import models

def import_session_data():
    # 1. Create Tables
    print("Creating tables...")
    try:
        models.Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error creating tables: {e}")

    db = SessionLocal()
    
    # 2. Schema Migration (Manual)
    # Check if mental_state column exists, if not add it
    try:
        from sqlalchemy import text
        db.execute(text("ALTER TABLE activity_logs ADD COLUMN mental_state VARCHAR"))
        db.commit()
        print("Migrated schema: Added mental_state column")
    except Exception as e:
        db.rollback()
        # Ignore if column already exists (Duplicate column name error)
        print(f"Schema migration note: {e}")
    
    csv_file = os.path.join("Database", "session_data.csv")
    if not os.path.exists(csv_file):
        print(f"File not found: {csv_file}")
        return

    print(f"Reading {csv_file}...")
    
    count = 0
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 2. Extract Project
            project_name = row['project_name']
            project = db.query(models.Project).filter(models.Project.name == project_name).first()
            if not project:
                # Create default project if not exists
                project = models.Project(
                    id=row['project_name'], # Use name as ID or generate one. FrontEnd uses name often. Let's use name as ID for simplicity or UUID.
                    # Models says ID is String.
                    name=project_name,
                    description=f"Imported {project_name} project",
                    color="#4F46E5", # Indigo default
                    status="Active"
                )
                db.add(project)
                db.commit() # Commit to get ID if generated (but we set it)
                db.refresh(project)
            
            # 3. Parse Timestamp
            # CSV: date (2026-01-10), start_time (09:00)
            dt_str = f"{row['date']} {row['start_time']}"
            timestamp = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
            
            # 4. Create ActivityLog
            # Map CSV fields to Model
            # cognitive_load: 0.42 -> 42
            cog_load = int(float(row['cognitive_load']) * 100)
            
            log = models.ActivityLog(
                project_id=project.id,
                timestamp=timestamp,
                keystrokes=int(row['keystroke_rate']),
                mouse_distance=float(row['mouse_activity']),
                active_window=f"{row['session_type']} - {project_name}", # inferred
                focus_score=int(row['focus_score']),
                cognitive_load=cog_load,
                mental_state=row['mental_state']
            )
            db.add(log)
            count += 1
            
    db.commit()
    db.close()
    print(f"Successfully imported {count} activity logs.")

if __name__ == "__main__":
    import_session_data()
