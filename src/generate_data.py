import numpy as np
import pandas as pd
import os

def generate_telemetry_data(n_samples=5000, random_state=42):
    np.random.seed(random_state)
    cpu_temp = np.random.normal(loc=65, scale=12, size=n_samples).clip(40, 105)
    ram_usage = np.random.uniform(20, 99, size=n_samples)
    disk_io_latency = np.random.exponential(scale=15, size=n_samples).clip(1, 120)
    packet_drop_rate = np.random.beta(a=0.5, b=10, size=n_samples) * 100
    uptime_hours = np.random.exponential(scale=200, size=n_samples).clip(1, 2000)

    risk_score = (
        (cpu_temp > 85).astype(int) * 3.0 +
        (ram_usage > 90).astype(int) * 2.5 +
        (disk_io_latency > 50).astype(int) * 2.0 +
        (packet_drop_rate > 15).astype(int) * 2.0 +
        np.random.normal(0, 1, size=n_samples)
    )
    
    failure = (risk_score > 4.5).astype(int)

    df = pd.DataFrame({
        "cpu_temp_celsius": np.round(cpu_temp, 2),
        "ram_usage_pct": np.round(ram_usage, 2),
        "disk_io_latency_ms": np.round(disk_io_latency, 2),
        "packet_drop_rate": np.round(packet_drop_rate, 2),
        "uptime_hours": np.round(uptime_hours, 1),
        "failure": failure
    })
    
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/server_telemetry.csv", index=False)
    return df

if __name__ == "__main__":
    generate_telemetry_data()