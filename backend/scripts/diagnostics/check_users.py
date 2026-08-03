from app.db.models import User
from app.db.session import SessionLocal
import traceback

def check_users():
    db = SessionLocal()
    
    try:
        users = db.query(User).all()
        print(f"Total Users: {len(users)}")
        for u in users:
            print(f"- {u.email} (ID: {u.id})")
            
        if not users:
            print("No users found! You need to seed the database.")
    except Exception as e:
        print("FULL ERROR TRACEBACK:")
        traceback.print_exc()
        print(f"Error Report: {e}")
        with open("error.log", "w") as f:
            f.write(traceback.format_exc())
    finally:
        db.close()

if __name__ == "__main__":
    check_users()
