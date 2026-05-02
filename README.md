# 🚀 Real-Time Failure Prediction System

A distributed, event-driven machine learning system for real-time failure prediction using Kafka, MLflow, FastAPI, and Redis.

---

## 🧠 Overview

This project simulates a production-grade ML pipeline where incoming system metrics are processed asynchronously to predict potential failures.

The architecture decouples ingestion, processing, and inference layers using Kafka, enabling scalability and non-blocking API responses.

---

## 🏗️ Architecture

```
Client
  ↓
FastAPI (API Layer)
  ↓
Kafka (Streaming Layer)
  ↓
Consumer (Processing + ML Inference)
  ↓
MLflow (Model Registry)
  ↓
Redis (Caching Layer)
  ↓
API (Result Retrieval)
```

---

## ⚙️ Tech Stack

* **Backend**: FastAPI
* **Streaming**: Apache Kafka
* **ML Lifecycle**: MLflow
* **Cache/Storage**: Redis
* **ML Models**: Scikit-learn (RandomForest, Logistic Regression)
* **Containerization**: Docker, Docker Compose
* **Monitoring**: Prometheus (basic metrics)

---

## 🚀 Features

* Real-time event-driven inference pipeline
* Asynchronous, non-blocking API design
* MLflow-based model versioning and deployment
* Redis caching for fast result retrieval
* Dockerized microservices architecture
* Scalable and decoupled system design

---

## 📂 Project Structure

```
P1/
│── api.py                # FastAPI service
│── consumer.py           # Kafka consumer + ML inference
│── train_model.py        # Model training + MLflow logging
│── requirements.txt
│── docker-compose.yml
│── Dockerfile
│── logger.py
│── data/
│── scripts/
```

---

## 🧪 How It Works

1. User sends system metrics via API
2. API publishes event to Kafka
3. Consumer reads event asynchronously
4. ML model predicts failure
5. Result stored in Redis
6. API returns result using request_id

---

## 📥 API Usage

### 🔹 Send Prediction Request

```bash
curl -X POST http://localhost:8000/predict \
-H "Content-Type: application/json" \
-d '{"cpu":90,"memory":85,"latency":200,"error_rate":0.2}'
```

### 🔹 Get Result

```bash
curl http://localhost:8000/result/<request_id>
```

---

## 📊 Example Input

```json
{
  "cpu": 90,
  "memory": 85,
  "latency": 200,
  "error_rate": 0.2
}
```

---

## 📊 Example Output

```json
{
  "result": {
    "status": "FAILURE",
    "causes": [["CPU", 90], ["MEMORY", 85]],
    "actions": ["Scale CPU", "Increase Memory"]
  }
}
```

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone <your-repo-link>
cd P1
```

---

### 2️⃣ Start services

```bash
docker-compose up --build
```

---

### 3️⃣ Train model

```bash
docker exec -it p1-api-1 python train_model.py
```

---

### 4️⃣ System is ready 🎉

---

## 🧠 Key Learnings

* Building distributed ML systems
* Kafka-based asynchronous processing
* MLflow model registry and versioning
* Docker container orchestration
* Debugging real-world system issues (networking, memory, services)

---

## ⚠️ Limitations

* Model is basic (focus is system design, not accuracy)
* No advanced fault tolerance (DLQ, retries not implemented yet)
* Limited monitoring

---

## 🚀 Future Improvements

* Add Dead Letter Queue (DLQ)
* Add retry mechanisms
* Integrate Grafana dashboard
* Automate model promotion in MLflow
* Improve model performance
* implement LLm Logic

---

## 👨‍💻 Author

Prince Jaiswal

