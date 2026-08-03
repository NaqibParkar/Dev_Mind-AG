
import sys
import os
from getpass import getpass

# Add current directory to sys.path
sys.path.append(os.getcwd())

try:
    from app.core.security import hash_password
    from app.db.models import User
    from app.db.session import SessionLocal
except ImportError:
    print("Run this script from the backend directory.")
    sys.exit(1)

def reset_password(email, new_password):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            print(f"User found: {user.email}")
            # Force set verification to True just in case
            user.is_verified = True
            # Update password
            user.hashed_password = hash_password(new_password)
            db.commit()
            print(f"Password has been reset to '{new_password}' for user {email}")
        else:
            print(f"User {email} not found. Creating it...")
            new_user = User(
                email=email,
                hashed_password=hash_password(new_password),
                full_name="Demo User",
                is_verified=True
            )
            db.add(new_user)
            db.commit()
            print(f"User {email} created with password '{new_password}'")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/diagnostics/debug_auth.py EMAIL")
    reset_password(sys.argv[1], getpass("New password: "))
