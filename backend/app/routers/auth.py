
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..core.security import create_access_token, hash_password, verify_password
from ..db.models import User
from ..db.session import get_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

class UserRegister(BaseModel):
    email: str
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = None


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    is_verified: bool


@router.post("/register", response_model=Token)
def register(user: UserRegister, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        full_name=user.full_name,
        is_verified=False,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "access_token": create_access_token(str(new_user.id)),
        "token_type": "bearer",
        "user_id": new_user.id,
        "is_verified": new_user.is_verified,
    }


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    try:
        is_valid = verify_password(user.password, db_user.hashed_password)
        if not is_valid:
            raise HTTPException(status_code=400, detail="Invalid credentials")
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials",
        ) from exc

    return {
        "access_token": create_access_token(str(db_user.id)),
        "token_type": "bearer",
        "user_id": db_user.id,
        "is_verified": db_user.is_verified,
    }


@router.get("/verify")
def verify_email(email: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.is_verified = True
    db.commit()
    return {"message": "Email verified successfully", "user": email}
