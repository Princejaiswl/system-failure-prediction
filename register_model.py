import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# sample dummy model (replace later with your real model)
X = np.random.rand(100, 4)
y = np.random.randint(0, 2, 100)

model = RandomForestClassifier()
model.fit(X, y)

mlflow.set_tracking_uri("http://localhost:5000")

with mlflow.start_run():
    mlflow.sklearn.log_model(model, "model")

    model_uri = "runs:/{}/model".format(mlflow.active_run().info.run_id)

    # Register model
    result = mlflow.register_model(model_uri, "FailureModel")

    print("Model registered:", result.name)
