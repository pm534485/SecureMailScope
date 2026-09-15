import joblib
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List

class MLInferenceEngine:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent.parent
        self.model_dir = self.base_dir / "data/models"
        
        self.model_path = self.model_dir / "risk_classifier.pkl"
        self.encoders_path = self.model_dir / "encoders.pkl"
        
        self.model = None
        self.encoders = None
        
        self.load_models()

    def load_models(self):
        if self.model_path.exists() and self.encoders_path.exists():
            self.model = joblib.load(self.model_path)
            self.encoders = joblib.load(self.encoders_path)

    def predict_risk(self, session: Dict[str, Any]) -> Dict[str, Any]:
        if not self.model or not self.encoders:
            return {"predicted_risk": "UNKNOWN", "confidence": 0.0, "error": "Model not loaded"}

        # Extract features from session
        tls = session.get("tls_info", {})
        starttls = session.get("starttls_info", {})
        
        cipher = tls.get("cipher_suite", "None")
        
        features = {
            'protocol': session.get("primary_protocol", "UNKNOWN"),
            'tls_version': tls.get("negotiated_version", "None"),
            'cipher_suite': cipher,
            'forward_secrecy': ("DHE" in cipher or "ECDHE" in cipher),
            'starttls_success': starttls.get("success", False),
            'certificate_expired': False, # Placeholder
            'certificate_self_signed': False, # Placeholder
            'duration': session.get("duration", 0),
            'packet_count': session.get("packet_count", 0)
        }
        
        df = pd.DataFrame([features])
        
        # Apply encoders gracefully
        for col in ['protocol', 'tls_version', 'cipher_suite']:
            if col in self.encoders:
                # Handle unseen labels by mapping to a default or 0
                try:
                    df[col] = self.encoders[col].transform(df[col].astype(str))
                except ValueError:
                    df[col] = 0
                    
        df = df.fillna(0).astype(float)
        
        prediction = self.model.predict(df)[0]
        probabilities = self.model.predict_proba(df)[0]
        confidence = max(probabilities) * 100
        
        return {
            "predicted_risk": prediction,
            "confidence": round(confidence, 2)
        }
