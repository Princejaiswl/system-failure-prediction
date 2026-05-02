from fastapi import FastAPI
from kafka import KafkaProducer
import json

app = FastAPI()

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/send")
def send_event(value: int):
    data = {"event": "api_event", "value": value}
    producer.send("test-json", data)
    return {"status": "sent", "data": data}
