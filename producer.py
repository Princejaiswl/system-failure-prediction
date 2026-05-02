from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for i in range(5):
    data = {"event": "test", "value": i}
    producer.send("test-json", data)
    print(f"Sent: {data}")
    time.sleep(1)

producer.flush()
