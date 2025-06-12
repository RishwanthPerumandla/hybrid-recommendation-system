import mlflow
from text_embedder import TextEmbedder
from image_embedder import ImageEmbedder
import numpy as np

mlflow.set_experiment("postrec-embedder-test")

with mlflow.start_run():
    text_encoder = TextEmbedder()
    image_encoder = ImageEmbedder()

    text = "Best hiking trail in the Alps!"
    image_url = "https://i.redd.it/2v9kdcx562i11.jpg"

    text_emb = text_encoder.encode(text)
    image_emb = image_encoder.encode(image_url)

    mlflow.log_metric("text_embedding_dim", len(text_emb))
    mlflow.log_metric("image_embedding_dim", len(image_emb))

    # Save a few embedding samples for inspection
    np.save("sample_text_emb.npy", text_emb)
    np.save("sample_image_emb.npy", image_emb)

    mlflow.log_artifact("sample_text_emb.npy")
    mlflow.log_artifact("sample_image_emb.npy")

    print("✅ Logged embeddings and metadata with MLflow.")
