from prometheus_client import Counter, Histogram, generate_latest
from fastapi import Response
import time
from fastapi import FastAPI
from pydantic import BaseModel
from kafka import KafkaProducer
import json
import redis
import time
import asyncio
import uuid
from logger import setup_logger

logger = setup_logger()

app = FastAPI()


REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total API Requests"
)

REQUEST_LATENCY = Histogram(
    "api_request_latency_seconds",
    "API Request Latency"
)




def create_producer():
    for i in range(30):
        try:
            producer = KafkaProducer(
                bootstrap_servers="kafka:9092",
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            print("✅ Connected to Kafka")
            return producer
        except Exception as e:
            print("⏳ Waiting for Kafka...")
            time.sleep(5)

    raise Exception("❌ Kafka not available")

producer = create_producer()



r = redis.Redis(host='redis', port=6379,password="mypassword", decode_responses=True)


class InputData(BaseModel):
    cpu: float
    memory: float
    latency: float
    error_rate: float


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")



@app.post("/predict")
async def predict(data: InputData):

    REQUEST_COUNT.inc()

    payload = data.dict()
    request_id = str(uuid.uuid4())
    payload["request_id"] = request_id

    logger.info(json.dumps({
        "type": "api_request",
        "request_id": request_id
    }))

    producer.send("test-json", payload)

    # ✅ DO NOT WAIT
    return {
        "status": "submitted",
        "request_id": request_id
    }

@app.get("/result/{request_id}")
def get_result(request_id: str):

    key = f"event:{request_id}"
    result = r.get(key)

    if result:
        return {"result": json.loads(result)}

    return {"status": "processing"}
