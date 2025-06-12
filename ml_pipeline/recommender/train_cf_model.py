import pandas as pd
import numpy as np
import mlflow
import joblib
import json
from pathlib import Path
from collections import defaultdict
from surprise import Dataset, Reader, SVD, accuracy
from surprise.model_selection import train_test_split

# --- Constants ---
DATA_PATH = Path("data/processed/interactions.csv")
MODEL_PATH = Path("ml_pipeline/recommender/cf_model.pkl")
RECS_PATH = Path("ml_pipeline/recommender/user_recommendations.json")
MLFLOW_EXPERIMENT = "postrec-collab-filtering"
TOP_N = 5
TEST_SIZE = 0.2
RANDOM_STATE = 42

# --- Load and prepare data ---
df = pd.read_csv(DATA_PATH)
reader = Reader(rating_scale=(0, 1))
data = Dataset.load_from_df(df[["user_id", "post_id", "interaction"]], reader)

# --- Train/Test Split ---
trainset, testset = train_test_split(data, test_size=TEST_SIZE, random_state=RANDOM_STATE)

# --- Start MLflow Experiment ---
mlflow.set_experiment(MLFLOW_EXPERIMENT)
with mlflow.start_run():
    mlflow.log_params({
        "model": "SVD",
        "top_n": TOP_N,
        "test_size": TEST_SIZE,
        "random_state": RANDOM_STATE
    })

    # --- Train Model ---
    algo = SVD()
    algo.fit(trainset)

    # --- Log dataset sizes ---
    mlflow.log_metrics({
        "train_size": len(list(trainset.all_ratings())),
        "test_size": len(testset)
    })

    # --- Evaluate on test set ---
    predictions = algo.test(testset)
    rmse = accuracy.rmse(predictions, verbose=False)
    mlflow.log_metric("RMSE", rmse)

    # --- Generate Top-N Recommendations ---
    def get_top_n(preds, n=5):
        top_n = defaultdict(list)
        for uid, iid, _, est, _ in preds:
            top_n[uid].append((iid, est))
        return {uid: [iid for iid, _ in sorted(user_ratings, key=lambda x: -x[1])[:n]]
                for uid, user_ratings in top_n.items()}

    anti_testset = trainset.build_anti_testset()
    top_n_recs = get_top_n(algo.test(anti_testset), n=TOP_N)

    # --- Save recommendations as JSON ---
    RECS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RECS_PATH, "w") as f:
        json.dump(top_n_recs, f, indent=2)
    mlflow.log_artifact(str(RECS_PATH))

    # --- Save model ---
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(algo, MODEL_PATH)
    mlflow.log_artifact(str(MODEL_PATH))

    print(f"✅ CF model trained and saved to {MODEL_PATH}")
    print(f"📊 RMSE: {rmse:.4f}")
    print(f"📁 Top-N recommendations saved to {RECS_PATH}")
