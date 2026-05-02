import pandas as pd
import numpy as np

metrics = pd.read_csv("data/raw/metrics.csv")

events = []

for _, row in metrics.iterrows():
    if np.random.rand() < 0.05:  # 5% chance of event
        event_type = np.random.choice([
            "deploy", "config_change", "restart"
        ])

        version = np.random.choice(["v1.0", "v1.1", "v2.0"])

        events.append([
            row["timestamp"],
            event_type,
            row["service"],
            version,
            "success"
        ])

event_df = pd.DataFrame(events, columns=[
    "timestamp", "event_type", "service", "version", "status"
])

event_df.to_csv("data/raw/events.csv", index=False)

print("Events generated")