def decide_action(row):
    actions = []

    # CPU issue
    if row["cpu"] > 85:
        actions.append(f"Scale up CPU for {row['service']} on {row['node']}")

    # Memory issue
    if row["memory"] > 90:
        actions.append(f"Restart {row['service']} on {row['node']}")

    # Latency issue
    if row["latency"] > 350:
        actions.append(f"Check network for {row['service']} on {row['node']}")

    # Event-based decision
    failure = row.get("failure", 0)
    if row["event_type"] == "deploy" and failure == 1:
        actions.append(f"Rollback deployment of {row['service']}")

    # Final fallback
    if not actions:
        actions.append("No action needed")

    return actions