# 📌 Post Recommendation System (Text + Image Hybrid)

A modern **hybrid recommendation system** that uses **textual (captions, hashtags)** and **visual (images)** information along with **user interactions** to recommend posts that users are most likely to engage with (like, comment, save).

---

## 🧠 Key Features

- **BERT / SBERT** for text embeddings
- **ResNet / Vision Transformer (ViT)** for image embeddings
- **Collaborative Filtering (KNN / NCF)** based on user interaction
- **Hybrid Fusion** of multimodal data
- **MLflow** for experiment tracking
- **MongoDB** as the backend store
- **FastAPI** for REST API
- **Dockerized** for easy deployment

---

## 📁 Project Structure

```
post-recommender/
├── backend/                     # FastAPI app
│   ├── main.py                 # FastAPI entrypoint
│   ├── routes/
│   └── utils/
│
├── ml_pipeline/                # All ML/DL logic
│   ├── embeddings/            # SBERT, ResNet, ViT embeddings
│   ├── recommender/           # Hybrid recommender logic
│   ├── trainer/               # Model training scripts
│   └── evaluator/             # Metrics: Precision@K, Recall@K
│
├── data/                       # Datasets
│   ├── raw/
│   └── processed/
│
├── mlruns/                     # MLflow tracking logs
│
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## 🚀 Tech Stack

| Layer         | Tech                          |
|---------------|-------------------------------|
| Language      | Python 3.10                   |
| API Framework | FastAPI                       |
| ML Framework  | PyTorch, HuggingFace, sklearn |
| Database      | MongoDB                       |
| Experiment    | MLflow, DVC (optional)        |
| Deployment    | Docker + Docker Compose       |

---

## 📋 TODOs & Milestones

### ✅ Part 1: Setup & Planning
- [x] Finalize project structure
- [x] Define schema for users, posts, interactions
- [x] Set up MongoDB connection in FastAPI
- [X] Initialize MLflow and test tracking

### 🚧 Part 2: Text + Image Embeddings
- [x] Build SBERT embedding generator
- [x] Build ResNet50 / ViT embedding extractor
- [x] Create pipeline to embed all posts
- [x] Store embeddings in MongoDB or vector store

### 🚧 Part 3: Collaborative Filtering
- [x] Prepare interaction matrix from likes
- [x] Train and evaluate Surprise/LightFM model
- [x] Serialize user latent factors

### 🚧 Part 4: Hybrid Recommender
- [x] Combine SBERT + ResNet + user embedding
- [x] Compute cosine similarity
- [x] Create FastAPI route for /recommendations

### 🚧 Part 5: MLflow + API Integration
- [x] Log experiments with MLflow
- [ ] Serve FastAPI routes with Docker
- [ ] Create dummy frontend (or use Postman for testing)

### 🚧 Part 6: MVP Deployment
- [ ] Write Dockerfile and docker-compose.yml
- [ ] Deploy to AWS EC2 (or Render)
- [ ] Test with simulated dataset

### 🚧 Part 7: Polish & Document
- [ ] Write case study for portfolio
- [ ] Add README visualizations
- [ ] Clean notebooks, scripts, and logs

---

## 💡 Future Enhancements
- Use Faiss / Pinecone for scalable vector similarity search
- Add comment-level interactions for richer feedback
- Train a Learning to Rank (LTR) model (e.g., LightGBM Ranker)
- Build a real frontend using React or Next.js

---

## 📜 License
MIT License

---

## 🧑‍💻 Author
**Rishwanth P**  
_Architecting intelligent recommender systems with vision & purpose._