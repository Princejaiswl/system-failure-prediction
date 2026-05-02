from kafka import KafkaProducer
import json
import pandas as pd
import time

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Load dataset
df = pd.read_csv("data/processed/final_dataset.csv")

print("🚀 Starting Data Stream...\n")

for _, row in df.iterrows():
    data = row.to_dict()

    print("📤 Sending:", data)

    # Send data to Kafka topic
    producer.send("test-json", data)

    # Ensure message is sent immediately
    producer.flush()

    # Simulate streaming delay
    time.sleep(0.5)
