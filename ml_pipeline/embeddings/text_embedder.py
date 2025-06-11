from sentence_transformers import SentenceTransformer
import numpy as np

class TextEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, text: str) -> np.ndarray:
        if not text:
            return np.zeros(384)
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding
