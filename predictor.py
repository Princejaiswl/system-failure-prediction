import joblib
import pandas as pd

model = joblib.load("model.pkl")

def predict_failure(row):
    features = ["cpu", "memory", "latency", "error_rate"]
    data = pd.DataFrame([row[features]])
    prediction = model.predict(data)[0]
    return prediction