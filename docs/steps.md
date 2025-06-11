Steps Followed

mkdir backend ml_pipeline data
python -m venv .venv
.venv\\Scripts\\activate on Windows


pip install fastapi uvicorn pymongo[srv] python-dotenv
pip install torch torchvision sentence-transformers
pip install scikit-learn mlflow


uvicorn backend.main:app --reload


The model SBERT (all-MiniLM-L6-v2) converted this into a 384-dimensional vector for text

The model ResNet50 (a deep CNN trained on ImageNet) extracted a 2048-dimensional vector for images

We tested both by using test_embedding.py

test_recommender.py
