# 📄 Content-Based Filtering - Technical Documentation

## 🎯 Objective
To build a **Content-Based Hybrid Post Recommendation System** that recommends social media posts (text + image) based on what a user has previously liked.

---

## ✅ What’s Built So Far

### 📦 Data Structure
- **Posts Collection**: Includes title, category, image, text embeddings (`text_emb`), and image embeddings (`image_emb`).
- **Likes Collection**: Tracks which users liked which posts.
- **Users Collection**: Optional user metadata.

### 🔍 Embedding Pipelines
- **Text Embeddings**:
  - Model: `sentence-transformers/all-MiniLM-L6-v2`
  - Output: 384-dimensional dense vector
  - Captures the semantic meaning of the post title and category

- **Image Embeddings**:
  - Model: Pretrained `ResNet50`
  - Output: 2048-dimensional dense vector
  - Captures high-level visual features

- **Final Vector (Hybrid)**: Concatenation of both embeddings
  - `final_vector = [text_emb || image_emb]` → Shape: `(2432,)`

### 🧠 Recommendation Logic (Content-Based)

1. **User Profile Creation**:
   - Aggregate all liked posts
   - Fetch their embeddings (text + image)
   - Average them to get the **user vector**

2. **Post Comparison**:
   - Exclude already liked posts
   - Fetch embeddings for all other posts
   - Compute **cosine similarity** between user vector and each post vector

3. **Ranking and Filtering**:
   - Sort by similarity score
   - Return top-K most similar posts

4. **Response Fields**:
   - `_id`, `title`, `category`, `post_type`, `image`
   - `similarity_score`: Numeric value (0–1)
   - `matched_reason`: Currently hardcoded as "Similar to your liked content"

---

## 📊 Math Behind It

### Cosine Similarity
Measures the angle between two vectors:
\[
\cos(\theta) = \frac{u \cdot v}{\|u\| \cdot \|v\|}
\]
- **u** = user preference vector
- **v** = candidate post vector
- Ranges from -1 (opposite) to 1 (exact match)

### Vector Representation
Each post = point in 2432D space
- Liked posts → define a preference direction
- New posts → matched by direction closeness

---

## 🧱 Code Modules Used

- `embed_text.py` → Generates text embeddings using SBERT
- `embed_image.py` → Generates image embeddings using ResNet
- `batch_embed_posts.py` → Applies embeddings to all posts in DB
- `recommender/content_recommender.py` → Core logic to generate recommendations
- `test_recommender.py` → Script to test functionality for a given user

---

## ✅ What Works Well
- Content understanding using BERT + CNN hybrid
- Embeddings stored directly in MongoDB
- Scalable structure for FastAPI integration
- User-facing metadata is filtered and clean

---

## 🗺️ What’s Next

### 📌 Short Term
- Integrate with Frontend
- Display similarity score and reason on UI
- Add post filters (e.g., category)

### 📈 Mid Term
- Include user behavior metrics (e.g., saves, shares)
- Add collaborative filtering
- Use ANN search with FAISS for scale

### 📦 Long Term
- Integrate MLflow for model versioning
- Full Docker-based deployment
- MLOps: CI/CD pipelines for embedding and recommendation updates

---

## 📬 Summary
I’ve built a **zero-shot hybrid recommender** that uses ML for embeddings, cosine similarity for ranking, and REST APIs for serving. It is extensible, explainable, and production-ready for small to mid-scale deployments.
