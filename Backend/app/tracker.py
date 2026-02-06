import threading
import time
import math # Added for distance calc
from datetime import datetime
try:
    from pynput import keyboard, mouse
except ImportError:
    keyboard = None
    mouse = None

from . import crud, schemas
from .database import SessionLocal
from .models import Project

class ActivityTracker:
    def __init__(self):
        self.keystrokes = 0
        self.mouse_distance = 0.0
        self.last_x = None # Track previous position
        self.last_y = None
        self._running = False
        self._lock = threading.Lock()
        
        self.keyboard_listener = None
        self.mouse_listener = None

    def get_current_stats(self):
        with self._lock:
            return {
                "keystrokes": self.keystrokes,
                "mouse_distance": self.mouse_distance
            }
        
    def _on_press(self, key):
        with self._lock:
            self.keystrokes += 1

    def _on_move(self, x, y):
        with self._lock:
            if self.last_x is not None and self.last_y is not None:
                # Calculate real pixel distance instead of just +1
                dist = math.sqrt((x - self.last_x)**2 + (y - self.last_y)**2)
                self.mouse_distance += dist
            self.last_x = x
            self.last_y = y

    def start(self):
        if not keyboard or not mouse:
            print("Pynput not available. Tracking disabled.")
            return
        self._running = True
        self.keyboard_listener = keyboard.Listener(on_press=self._on_press)
        self.mouse_listener = mouse.Listener(on_move=self._on_move)
        self.keyboard_listener.start()
        self.mouse_listener.start()
        
        # CHANGED: Faster loop for "Live" feel
        self.thread = threading.Thread(target=self._logging_loop, daemon=True)
        self.thread.start()
        print("Activity Tracker Started - Logging every 5 seconds")

    def _logging_loop(self):
        while self._running:
            time.sleep(5) # CHANGED from 60 to 5 seconds
            
            with self._lock:
                current_keystrokes = self.keystrokes
                current_mouse = int(self.mouse_distance) # Convert to int
                self.keystrokes = 0
                self.mouse_distance = 0
            
            # Always log if running to keep the "Live" chart moving
            self._save_to_db(current_keystrokes, current_mouse)

    def _save_to_db(self, keystrokes, mouse_dist):
        try:
            db = SessionLocal()
            active_project = db.query(Project).filter(Project.status == "Active").first()
            project_id = active_project.id if active_project else None
            
            # Ensure your schema matches these names!
            activity = schemas.ActivityData(
                timestamp=datetime.utcnow(),
                keystrokes=keystrokes,
                mouse_distance=mouse_dist,
                active_window="Active Window", 
                project_id=project_id
            )
            crud.log_activity(db, activity)
            db.close()
        except Exception as e:
            print(f"Error logging: {e}")