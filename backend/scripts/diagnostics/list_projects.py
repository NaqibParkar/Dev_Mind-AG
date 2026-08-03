from app.db.models import Project
from app.db.session import SessionLocal

db = SessionLocal()
projects = db.query(Project).all()
print(f"Found {len(projects)} projects:")
for p in projects:
    print(f"- ID: {p.id}, Name: {p.name}, Status: {p.status}")
db.close()
