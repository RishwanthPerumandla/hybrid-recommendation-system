import pandas as pd
import numpy as np
import mlflow
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from collections import defaultdict
from pathlib import Path
import json

# Load data
df = pd.read_csv("data/processed/interactions.csv")
reader = Reader(rating_scale=(0, 1))
data = Dataset.load_from_df(df[["user_id", "post_id", "interaction"]], reader)

# Start MLflow
mlflow.set_experiment("postrec-collab-filtering")
with mlflow.start_run():
    mlflow.log_param("model", "SVD")
    
    # Train/test split
    trainset, testset = train_test_split(data, test_size=0.2)
    algo = SVD()
    algo.fit(trainset)
    mlflow.log_metric("train_size", len(list(trainset.all_ratings())))
    mlflow.log_metric("test_size", len(testset))

    # Predict and evaluate
    predictions = algo.test(testset)

    # Compute RMSE
    from surprise import accuracy
    rmse = accuracy.rmse(predictions)
    mlflow.log_metric("RMSE", rmse)

    # Generate top-N recommendations
    def get_top_n(predictions, n=5):
        top_n = defaultdict(list)
        for uid, iid, true_r, est, _ in predictions:
            top_n[uid].append((iid, est))
        for uid in top_n:
            top_n[uid] = sorted(top_n[uid], key=lambda x: x[1], reverse=True)[:n]
        return top_n

    anti_testset = trainset.build_anti_testset()
    full_preds = algo.test(anti_testset)
    top_n = get_top_n(full_preds, n=5)

    # Save to JSON
    recs = {uid: [iid for iid, _ in items] for uid, items in top_n.items()}
    out_path = Path("ml_pipeline/recommender/user_recommendations.json")
    with open(out_path, "w") as f:
        json.dump(recs, f, indent=2)
    mlflow.log_artifact(str(out_path))

    print("✅ Collaborative Filtering complete.")

import joblib
from pathlib import Path

# ✅ Save model to disk
model_path = Path("ml_pipeline/recommender/cf_model.pkl")
model_path.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(algo, model_path)

# ✅ Also log to MLflow
mlflow.log_artifact(str(model_path))

print(f"✅ Model saved to {model_path}")
