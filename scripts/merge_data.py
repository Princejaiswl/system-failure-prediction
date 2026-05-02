import pandas as pd

metrics = pd.read_csv("data/raw/metrics.csv")
logs = pd.read_csv("data/raw/logs.csv")
events = pd.read_csv("data/raw/events.csv")

# Merge metrics + logs
df = pd.merge(metrics, logs, on=["timestamp", "service", "node"], how="left")

# Merge events
df = pd.merge(df, events, on=["timestamp", "service"], how="left")

# Fill missing
df.fillna({
    "event_type": "none",
    "version": "none",
    "status": "none"
}, inplace=True)

# Create failure label
df["failure"] = (
    (df["cpu"] > 90) &
    (df["error_rate"] > 0.2)
).astype(int)

df.to_csv("data/processed/final_dataset.csv", index=False)

print("Final dataset ready")