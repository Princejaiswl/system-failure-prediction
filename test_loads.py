import requests
import threading

url = "http://127.0.0.1:8000/predict"

import random

def generate_payload():
    if random.random() > 0.5:
        # FAILURE case
        return {
            "cpu": random.randint(85, 100),
            "memory": random.randint(80, 100),
            "latency": random.randint(150, 300),
            "error_rate": round(random.uniform(0.15, 0.4), 2)
        }
    else:
        # HEALTHY case
        return {
            "cpu": random.randint(20, 70),
            "memory": random.randint(30, 70),
            "latency": random.randint(50, 150),
            "error_rate": round(random.uniform(0.01, 0.08), 2)
        }



def send_request(i):
    payload = generate_payload()   # ✅ generate per request
    print(f"Payload {i}: {payload}")  # debug

    response = requests.post(url, json=payload)
    print(f"Request {i}: {response.json()}")

threads = []

for i in range(10):  # 👈 only 10 requests
    t = threading.Thread(target=send_request, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
