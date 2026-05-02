import pandas as pd
import numpy as np

np.random.seed(42)

rows = 5000

data = {
    "timestamp": pd.date_range(start="2024-01-01", periods=rows, freq="T"),
    "cpu": np.random.normal(60, 20, rows).clip(0, 100),
    "memory": np.random.normal(65, 15, rows).clip(0, 100),
    "latency": np.random.normal(200, 50, rows).clip(50, 500),
    "error_rate": np.random.uniform(0, 0.3, rows),
    "service": np.random.choice(["auth", "payment", "search"], rows),
    "node": np.random.choice(["node1", "node2", "node3"], rows)
}

df = pd.DataFrame(data)
df.to_csv("data/raw/metrics.csv", index=False)

print("Metrics generated")