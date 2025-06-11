from ml_pipeline.embeddings.text_embedder import TextEmbedder
from ml_pipeline.embeddings.image_embedder import ImageEmbedder

# 1. Text embedding
text_model = TextEmbedder()
text = "Sunset over a mountain lake #nature #travel"
text_emb = text_model.encode(text)
print("📄 Text embedding (first 5 values):", text_emb[:5])
print("Text vector shape:", text_emb.shape)  # Should be (384,)

# 2. Image embedding
image_model = ImageEmbedder()

# Make sure you have sample_image.txt containing the base64 string
with open("sample_image.txt", "r") as f:
    base64_image = f.read()

image_emb = image_model.encode(base64_image)
print("🖼️ Image embedding (first 5 values):", image_emb[:5])
print("Image vector shape:", image_emb.shape)  # Should be (2048,)
