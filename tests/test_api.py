import requests
import time
import sys

BASE_URL = "http://localhost:8000"

def run_smoke_test():
    print("Waiting for Docker container to initialize...")
    time.sleep(5) 

    # 1. Test Health Endpoint
    print("\n--- Pinging /health ---")
    health = requests.get(f"{BASE_URL}/health")
    if health.status_code == 200:
        print("SUCCESS: API is up and healthy.")
    else:
        print("FAILED: API health check failed.")
        sys.exit(1)

    # 2. Test Prediction Endpoint (Simulate an attack)
    print("\n--- Sending simulated attack to /predict ---")
    attack_payload = {
        "bytes_per_packet": 64.0,
        "connection_duration_ms": 6000.0,
        "failed_logins": 8.0
    }
    
    predict = requests.post(f"{BASE_URL}/predict", json=attack_payload)
    if predict.status_code == 200:
        result = predict.json()
        print(f"SUCCESS: API Response -> {result['status']}")
        # Fail the test if it doesn't recognize an obvious attack
        if result['threat_level'] != 1:
            print("FAILED: Model failed to detect the intrusion!")
            sys.exit(1)
    else:
        print("FAILED: Predict endpoint crashed.")
        sys.exit(1)

if __name__ == "__main__":
    run_smoke_test()