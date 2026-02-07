from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Neon DB Connection String provided by user
# Note: Removed channel_binding=require for broad compatibility, sslmode=require is usually sufficient for Neon.
# If strict SCRAM-SHA-256-PLUS is enforced and fails, we can add it back.
SQLALCHEMY_DATABASE_URL = "postgresql://neondb_owner:npg_lcQCqBKU3n5F@ep-rapid-voice-a1jyo0em-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
