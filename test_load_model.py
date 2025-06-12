# test_load_model.py
import joblib

model = joblib.load("ml_pipeline/recommender/cf_model.pkl")
print("✅ Model loaded:", model)
