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
import ctypes
from ctypes import wintypes

def get_active_window():
    try:
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        if length == 0:
            return "Unknown"
        buff = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
        # print(f"DEBUG: Active Window: {buff.value}") # Uncomment for debugging
        return buff.value
    except Exception as e:
        print(f"Error getting window: {e}")
        return "Unknown"

class ActivityTracker:
    def __init__(self):
        self.keystrokes = 0
        self.mouse_distance = 0.0
        self.last_x = None # Track previous position
        self.last_y = None
        self._running = False
        self._lock = threading.Lock()
        
        self.mouse_listener = None
        
        # New: Context Switch Tracking
        self.context_switches = 0
        self.current_window = "Unknown"
        
        # New: Cumulative Stats for Live UI
        self.total_keystrokes = 0
        self.total_mouse_distance = 0.0

    def get_current_stats(self):
        with self._lock:
            return {
                "keystrokes": self.keystrokes,
                "mouse_distance": self.mouse_distance,
                "total_keystrokes": self.total_keystrokes,
                "total_mouse_distance": self.total_mouse_distance,
                "active_window": self.current_window, 
                "context_switches": self.context_switches
            }
        
    def _on_press(self, key):
        with self._lock:
            self.keystrokes += 1
            self.total_keystrokes += 1

    def _on_move(self, x, y):
        try:
            with self._lock:
                if self.last_x is not None and self.last_y is not None:
                    # Calculate real pixel distance instead of just +1
                    dist = math.sqrt((x - self.last_x)**2 + (y - self.last_y)**2)
                    self.mouse_distance += dist
                    self.total_mouse_distance += dist
                self.last_x = x
                self.last_y = y
        except Exception as e:
            print(f"Mouse listener error: {e}")

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
        
        # New: Window Monitor Thread (Fast Poll)
        self.monitor_thread = threading.Thread(target=self._monitor_window_loop, daemon=True)
        self.monitor_thread.start()
        
        print("Activity Tracker Started - Logging every 5 seconds")

    def _monitor_window_loop(self):
        """Polls active window frequently to catch switches."""
        last_window = "Unknown"
        while self._running:
            time.sleep(0.5) # Check every 500ms
            
            try:
                new_window = get_active_window()
                
                # Update current window securely
                with self._lock:
                    self.current_window = new_window
                    
                # Detect switch (ignore Unknown/Empty)
                if new_window and new_window != "Unknown" and new_window != last_window:
                    if last_window != "Unknown": # Don't count initialization as a switch
                         with self._lock:
                             self.context_switches += 1
                    last_window = new_window
                    
            except Exception as e:
                print(f"Monitor error: {e}")

    def _logging_loop(self):
        while self._running:
            time.sleep(5) # CHANGED from 60 to 5 seconds
            
            with self._lock:
                current_keystrokes = self.keystrokes
                current_mouse = int(self.mouse_distance) # Convert to int
                # self.keystrokes = 0 # Don't reset for live view? 
                # Actually we DO want to reset for DB log, but maybe keep cumulative for live?
                # The current implementation resets. Let's keep it consistent.
                # Live view calculates delta.
                
                # We need to snapshot context switches for logging or just accumulate?
                # For now, let's keep context_switches cumulative for the session.
                pass 
                
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
            # Use cached window or get new? Cached is fine.
            with self._lock:
                current_window = self.current_window
            activity = schemas.ActivityData(
                timestamp=datetime.utcnow(),
                keystrokes=keystrokes,
                mouse_distance=mouse_dist,
                active_window=current_window if current_window else "Idle", 
                project_id=project_id,
                # Add dummy values for required fields if any (schema defaults to 0 mostly)
            )
            crud.log_activity(db, activity)
            db.close()
        except Exception as e:
            print(f"Error logging: {e}")