import pandas as pd
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import joblib

mlflow.set_tracking_uri("http://mlflow:5000")

# =========================
# Load + Transform
# =========================
df = pd.read_csv("data/processed/final_dataset.csv")

df["cpu_usage"] = df["cpu"]
df["memory_usage"] = df["memory"]
df["network_latency"] = df["latency"]
df["disk_io"] = 50

FEATURES = [
    "cpu_usage",
    "memory_usage",
    "disk_io",
    "network_latency",
    "error_rate"
]

X = df[FEATURES]
y = df["failure"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# Models
# =========================
models = {
    "RandomForest": RandomForestClassifier(),
    "LogisticRegression": LogisticRegression(max_iter=1000),
    }

best_model = None
best_score = 0

# =========================
# MLflow Experiment
# =========================
mlflow.set_experiment("Failure Prediction")

for name, model in models.items():

    with mlflow.start_run(run_name=name):

        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        acc = accuracy_score(y_test, preds)
        precision = precision_score(y_test, preds, zero_division=0)
        recall = recall_score(y_test, preds, zero_division=0)
        f1 = f1_score(y_test, preds, zero_division=0)

        # ✅ Log model type
        mlflow.log_param("model_type", name)

        # ✅ Log metrics
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)

        print(f"\n{name} → F1: {f1}")

        # Select best model
        if f1 > best_score:
            best_score = f1
            best_model = model
            best_name = name

# Save best model
with mlflow.start_run(run_name="BestModel"):

    mlflow.log_param("best_model", best_name)
    mlflow.log_metric("best_f1", best_score)

    mlflow.sklearn.log_model(
        sk_model=best_model,
        artifact_path="model",
        registered_model_name="FailureModel"   # 🔥 registers best model
    )


client = MlflowClient()

latest = client.get_latest_versions("FailureModel")[0].version

client.set_registered_model_alias(
    name="FailureModel",
    alias="production",
    version=latest
)

print("✅ Alias 'production' set to version:", latest)
    print(f"\n✅ Best model registered: {best_name}")

