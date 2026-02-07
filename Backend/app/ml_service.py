
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

MODEL_PATH = "burnout_model.joblib"

class BurnoutPredictor:
    def __init__(self):
        self.model = None
        self.is_trained = False
        self._train_model()

    def _train_model(self):
        # Try to load existing data
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Database", "session_data.csv")
        
        if os.path.exists(data_path):
            try:
                df = pd.read_csv(data_path)
                # print("Training on real data...")
                # Feature Engineering from CSV columns
                # We need features: cognitive_load, focus_score, keystrokes (rate?), mouse (activity?)
                # CSV has: cognitive_load, focus_score, keystroke_rate, mouse_activity, mental_state
                
                features = df[['cognitive_load', 'focus_score', 'keystroke_rate', 'mouse_activity']]
                target = df['mental_state']
                
                # Map target to Risk Level for simpler UI consumption if needed, or just use raw classes
                # Let's keep raw classes but ensure we map them to High/Med/Low in the API
                
                X = features.fillna(0)
                y = target
                
                self.model = RandomForestClassifier(n_estimators=100, random_state=42)
                self.model.fit(X, y)
                self.is_trained = True
                # joblib.dump(self.model, MODEL_PATH) 
                return
            except Exception as e:
                print(f"Failed to train on CSV: {e}")
        
        # Fallback: Synthetic Training Data
        print("Training on synthetic data...")
        # Generate synthetic data
        # Logic: High Load + Low Focus = Burnout
        #        Med Load + Med Focus = Distracted
        #        Low Load + High Focus = Flow
        
        n_samples = 1000
        cognitive_load = np.random.uniform(0, 100, n_samples)
        focus_score = np.random.uniform(0, 100, n_samples)
        keystrokes = np.random.uniform(0, 500, n_samples) # rate per min
        mouse = np.random.uniform(0, 1000, n_samples)
        
        X = pd.DataFrame({
            'cognitive_load': cognitive_load,
            'focus_score': focus_score,
            'keystroke_rate': keystrokes,
            'mouse_activity': mouse
        })
        
        y = []
        for i in range(n_samples):
            cl = cognitive_load[i]
            fs = focus_score[i]
            
            if cl > 70 and fs < 40:
                y.append("High Risk")
            elif cl > 50 and fs < 60:
                y.append("Moderate Risk")
            elif fs > 80:
                y.append("Low Risk") # Flow
            else:
                y.append("Low Risk")
                
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.model.fit(X, y)
        self.is_trained = True

    def predict(self, cognitive_load, focus_score, keystrokes, mouse_dist):
        if not self.is_trained:
            return "Unknown"
            
        # Create DF for single prediction
        input_data = pd.DataFrame([{
            'cognitive_load': cognitive_load,
            'focus_score': focus_score,
            'keystroke_rate': keystrokes,
            'mouse_activity': mouse_dist
        }])
        
        try:
            prediction = self.model.predict(input_data)[0]
            return prediction
        except Exception as e:
            print(f"Prediction error: {e}")
            return "Error"

# Global instance
predictor = BurnoutPredictor()
