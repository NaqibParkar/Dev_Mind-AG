from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, models, schemas, database
from ..models import User
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional

# Setup Pwd Context (Duplicated for now, should be in a utils file)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

class UserRegister(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    is_verified: bool

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/register", response_model=Token)
def register(user: UserRegister, db: Session = Depends(database.get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create User
    # In a real Neon Auth scenario, we might offload this to Neon's Auth API or use standard DB insert + trigger.
    # We'll stick to standard DB insert for "Neon DB" usage.
    new_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name,
        is_verified=False # Requires verification
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Simulate sending verification email (Log to console)
    print(f"--- SIMULATED EMAIL TO {user.email} ---")
    print(f"Please verify your email: http://localhost:8000/auth/verify?email={user.email}")
    print("---------------------------------------")
    
    return {
        "access_token": "mock_token_registered",
        "token_type": "bearer",
        "user_id": new_user.id,
        "is_verified": new_user.is_verified
    }

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(database.get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
        
    return {
        "access_token": "mock_token_login",
        "token_type": "bearer",
        "user_id": db_user.id,
        "is_verified": db_user.is_verified
    }

@router.get("/verify")
def verify_email(email: str, db: Session = Depends(database.get_db)):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.is_verified = True
    db.commit()
    return {"message": "Email verified successfully", "user": email}
