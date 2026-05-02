# =========================
# 1. ROW-BASED RCA (KEEP THIS)
# =========================
def find_root_cause(row):
    score_map = {}

    if row["cpu"] > 85:
        score_map["High CPU usage"] = 0.7

    if row["memory"] > 90:
        score_map["Memory overload"] = 0.8

    if row["latency"] > 350:
        score_map["Network latency spike"] = 0.75

    if row["error_rate"] > 0.2:
        score_map["High error rate"] = 0.85

    if row["log_level"] == "CRITICAL":
        score_map[row["message"]] = 0.9
    elif row["log_level"] == "ERROR":
        score_map[row["message"]] = 0.8

    if row["event_type"] == "deploy":
        score_map["Recent deployment issue"] = 0.88

    if row["cpu"] > 85 and row["latency"] > 300:
        score_map["CPU bottleneck causing latency"] = 0.92

    if row["memory"] > 90 and row["error_rate"] > 0.2:
        score_map["Memory leak causing failures"] = 0.95

    if not score_map:
        return [("No clear root cause", 0.5)]

    return sorted(score_map.items(), key=lambda x: x[1], reverse=True)


# =========================
# 2. TIME-BASED RCA (NEW)
# =========================
def find_root_cause_with_history(history):

    if len(history) < 3:
        return [("Not enough data for trend analysis", 0.4)]

    score_map = {}
    recent = history[-1]

    cpu_values = [r["cpu"] for r in history]
    error_values = [r["error_rate"] for r in history]
    latency_values = [r["latency"] for r in history]

    if cpu_values[-1] > cpu_values[0]:
        score_map["CPU increasing trend"] = 0.85

    if error_values[-1] > error_values[0]:
        score_map["Error rate increasing"] = 0.88

    if latency_values[-1] > latency_values[0]:
        score_map["Latency increasing"] = 0.8

    if cpu_values[-1] > 85 and error_values[-1] > 0.2:
        score_map["System overload due to CPU spike"] = 0.92

    for r in history:
        if r["event_type"] == "deploy":
            score_map["Recent deployment may have caused instability"] = 0.9
            break

    # 🔥 THIS LINE caused your error — now fixed because function exists
    row_causes = find_root_cause(recent)

    for cause, score in row_causes:
        score_map[cause] = score

    if not score_map:
        return [("No strong root cause detected", 0.5)]

    return sorted(score_map.items(), key=lambda x: x[1], reverse=True)