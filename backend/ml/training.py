import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os
from pathlib import Path

# Fix relative path if run from scripts
base_dir = Path(__file__).resolve().parent.parent.parent

def train_risk_model():
    data_path = base_dir / "data/features/synthetic_dataset.json"
    if not data_path.exists():
        print(f"Data file {data_path} not found.")
        return

    with open(data_path, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # Feature Engineering
    features = ['protocol', 'tls_version', 'cipher_suite', 'forward_secrecy', 
                'starttls_success', 'certificate_expired', 'certificate_self_signed', 
                'duration', 'packet_count']
    
    target = 'risk_label'

    X = df[features]
    y = df[target]

    # Encoding
    encoders = {}
    
    # Create a copy to avoid SettingWithCopyWarning
    X = X.copy()
    
    for col in ['protocol', 'tls_version', 'cipher_suite']:
        le = LabelEncoder()
        # Ensure we are assigning integers to a column that can hold them
        encoded_vals = le.fit_transform(X[col].astype(str))
        X[col] = encoded_vals.astype(int)
        encoders[col] = le

    # Fill NaN and convert booleans
    X = X.fillna(0)
    X = X.astype(float)

    # Train Random Forest
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)

    # Save models
    model_dir = base_dir / "data/models"
    model_dir.mkdir(parents=True, exist_ok=True)
    
    joblib.dump(clf, model_dir / "risk_classifier.pkl")
    joblib.dump(encoders, model_dir / "encoders.pkl")
    
    print("Risk Classification Model Trained Successfully.")

if __name__ == "__main__":
    train_risk_model()
