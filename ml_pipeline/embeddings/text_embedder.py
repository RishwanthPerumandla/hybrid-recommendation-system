from sentence_transformers import SentenceTransformer
import numpy as np
import mlflow


class TextEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

        # Log model name
        mlflow.log_param("text_encoder", model_name)

    def encode(self, text: str) -> np.ndarray:
        if not text:
            mlflow.log_metric("empty_text_count", 1)
            return np.zeros(384)

        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding
