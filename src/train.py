import os
import joblib
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier

def generate_network_data(n_samples=2000):
    """Generates synthetic network traffic data."""
    np.random.seed(42)
    # Features: bytes_per_packet, connection_duration_ms, failed_logins
    normal = np.random.normal(loc=[500, 150, 0], scale=[100, 50, 0.1], size=(n_samples, 3))
    # Malicious traffic (e.g., DDoS or brute force) has smaller packets, longer duration, or high failed logins
    malicious = np.random.normal(loc=[60, 5000, 5], scale=[20, 1000, 2], size=(n_samples // 4, 3))
    
    X = np.vstack([normal, malicious])
    y = np.array([0]*n_samples + [1]*(n_samples // 4)) # 0 = Normal, 1 = Intrusion
    return pd.DataFrame(X, columns=["bytes_per_packet", "connection_duration_ms", "failed_logins"]), y

def main():
    print("1. Generating Network Traffic Data...")
    X, y = generate_network_data()
    
    print("2. Training Decision Tree Classifier...")
    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    model.fit(X, y)
    
    print("3. Saving Model Artifact...")
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/intrusion_model.pkl")
    print("Model saved to models/intrusion_model.pkl")

if __name__ == "__main__":
    main()