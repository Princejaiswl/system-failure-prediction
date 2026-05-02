import pandas as pd

metrics = pd.read_csv("data/raw/metrics.csv")

logs = []

for _, row in metrics.iterrows():
    log_level = "INFO"
    message = "Normal operation"

    if row["cpu"] > 85:
        log_level = "WARN"
        message = "High CPU usage detected"

    if row["memory"] > 90:
        log_level = "ERROR"
        message = "Memory leak suspected"

    if row["latency"] > 350:
        log_level = "CRITICAL"
        message = "Service timeout"

    logs.append([
        row["timestamp"],
        row["service"],
        row["node"],
        log_level,
        message
    ])

log_df = pd.DataFrame(logs, columns=[
    "timestamp", "service", "node", "log_level", "message"
])

log_df.to_csv("data/raw/logs.csv", index=False)

print("Logs generated")