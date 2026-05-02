from kafka import KafkaConsumer
import json
import pandas as pd
import redis
from logger import setup_logger
import traceback
import joblib
import mlflow
import time
import mlflow.sklearn
# =========================
# 🔹 Load ML Model
# =========================
print("🚀 Consumer process started")

while True:
    try:
        print("🔄 Trying to load model from MLflow...")
        model = mlflow.sklearn.load_model("models:/FailureModel@production")
        print("✅ Model loaded successfully!")
        break
    except Exception as e:
        print(f"⏳ MLflow not ready yet: {e}")
        time.sleep(5)

print("🔥 Reached after model load")

## from logger import setup_logger

logger = setup_logger()

	
#dataset me data thoda laag format me hogya tha
#def transform_event(event):
 #   return {
  #      "cpu_usage": event.get("cpu"),
   #     "memory_usage": event.get("memory"),
    #    "disk_io": 50,  # default since not available
     #   "network_latency": event.get("latency"),
      #  "error_rate": event.get("error_rate")
    #}


# =========================
# 🔹 Validation (SAFE)
# =========================
def validate_event(event):
    required_fields = [
        "cpu_usage",
        "memory_usage",
        "disk_io",
        "network_latency",
        "error_rate"
    ]

    # Check missing keys
    missing = [f for f in required_fields if f not in event]
    if missing:
        print(f"⚠️ Missing fields: {missing}")
        return False

    # Check None values
    if any(event[f] is None for f in required_fields):
        print("⚠️ Skipping due to None values")
        return False

    # Check type
    for field in required_fields:
        if not isinstance(event[field], (int, float)):
            print(f"⚠️ Invalid type for {field}")
            return False

    return True

# =========================
# 🔹 Root Cause Analysis
# =========================
def root_cause(event):
    causes = []

    if event["cpu_usage"] > 85:
        causes.append(("CPU", event["cpu_usage"]))
    if event["memory_usage"] > 80:
        causes.append(("MEMORY", event["memory_usage"]))
    if event["error_rate"] > 0.1:
        causes.append(("ERROR", event["error_rate"]))

    return causes


# =========================
# 🔹 Decision Engine
# =========================
def decision_engine(causes):
    actions = []

    for c, value in causes:
        if c == "CPU":
            actions.append("Scale CPU")
        elif c == "MEMORY":
            actions.append("Increase Memory")
        elif c == "ERROR":
            actions.append("Restart Service")

    return actions


# =========================
# 🔹 Full Processing Pipeline
# =========================

def process_event(event):

    features = pd.DataFrame([{
        "cpu_usage": event["cpu_usage"],
        "memory_usage": event["memory_usage"],
        "disk_io": event["disk_io"],
        "network_latency": event["network_latency"],
        "error_rate": event["error_rate"]
    }])

    prediction = model.predict(features)[0]

    if (prediction == 1 or event["cpu_usage"] > 85 or event["memory_usage"] > 80 or event["error_rate"] > 0.1):
        causes = root_cause(event)
        actions = decision_engine(causes)

        return {
            "status": "FAILURE",
            "causes": causes,
            "actions": actions
        }

    return {"status": "HEALTHY"}


# =========================
# 🔹 Redis Connection
def transform_event(event):
    return {
        "cpu_usage": event["cpu"],
        "memory_usage": event["memory"],
        "disk_io": 50,
        "network_latency": event["latency"],
        "error_rate": event["error_rate"],
        "request_id": event.get("request_id")  # ✅ IMPORTANT
    }# =========================
r = redis.Redis(host='redis', port=6379,password="mypassword", decode_responses=True)


# =========================
# 🔹 Kafka Consumer
# =========================
while True:
    try:
        print("🔄 Connecting to Kafka...")
        consumer = KafkaConsumer(
            "test-json",
            bootstrap_servers="kafka:9092",
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="latest",
            group_id="consumer-group"
        )
        print("✅ Connected to Kafka")
        break
    except Exception as e:
        print("⏳ Kafka not ready:", e)
        time.sleep(5)
# =========================
# 🔹 Main Loop
# =========================

try:
    for message in consumer:
        print("📥 Received message:", message.value)
        try:
            raw_data = message.value
            data = transform_event(raw_data)

            logger.info(json.dumps({
                "type": "raw_event",
                "request_id": raw_data.get("request_id"),
                "cpu": raw_data.get("cpu"),
                "memory": raw_data.get("memory"),
                "latency": raw_data.get("latency"),
                "error_rate": raw_data.get("error_rate")
            }))

            print(f"🔄 Transformed: {data}")

            # ✅ Skip invalid data
            if not validate_event(data):
                continue

            # ✅ Skip dataset events (no request_id)
            if data.get("request_id") is None:
                print("⏭️ Skipping dataset event")
                continue

            # ✅ Process event
            result = process_event(data)

            logger.info(json.dumps({
                "type": "decision",
                "status": result["status"],
                "causes": result.get("causes"),
                "actions": result.get("actions"),
                "request_id": data.get("request_id"),
                "cpu": data.get("cpu_usage"),
                "memory": data.get("memory_usage")
            }))

            # ✅ Store in Redis
            request_id = data.get("request_id", "unknown")
            key = f"event:{request_id}"
            r.setex(key, 300, json.dumps(result))  # expires in 5 minutes

            print(f"💾 Stored in Redis → {key}")

        except Exception as e:
            logger.error(f"ERROR: {str(e)}")
            traceback.print_exc()

except KeyboardInterrupt:
    print("\n🛑 Consumer stopped manually")

finally:
    consumer.close()
    print("✅ Kafka consumer closed")# =========================
