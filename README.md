# 🔮 Hybrid Post Recommendation System

A full-stack, multimodal post recommendation system combining **content-based** (text + image) and **collaborative filtering** techniques. This project is built to serve personalized post suggestions for social platforms or content-driven apps.

## 🧠 Features

* 🔍 **Content-Based Recommendations**: Uses hybrid text + image embeddings and cosine similarity.
* 🡥 **Collaborative Filtering**: Matrix factorization (SVD) via `Surprise`, trained on user-post interactions.
* ⚖️ **Hybrid Recommendations**: Blends both methods for more diverse and accurate results.
* ⚡ **FastAPI Backend**: Modular, clean routes for users, likes, and recommendations.
* 🌐 **React Frontend (MUI + Vite)**: Clean dashboard with tabbed views and pagination.
* 📈 **MLflow Tracking**: All model metrics and artifacts are logged for reproducibility.

---

## 🏗️ Tech Stack

| Layer                 | Technology                    |
| --------------------- | ----------------------------- |
| Frontend              | React + Vite + Material UI    |
| Backend               | FastAPI                       |
| ML/NLP                | NumPy, Scikit-learn, Surprise |
| DB                    | MongoDB                       |
| MLOps                 | MLflow                        |

---

## 📂 Project Structure

```
.
├── backend/
│   ├── main.py
│   ├── routes/
│   ├── database.py
│   └── ...
├── ml_pipeline/
│   ├── recommender/
│   │   ├── content_recommender.py
│   │   └── ...
│   └── train_collab_model.py
├── data/
│   └── processed/
├── frontend/
│   ├── src/
│   ├── pages/
│   └── components/
└── README.md
```

---

## 🚀 How to Run

### 1. Clone the repo

```bash
git clone https://github.com/RishwanthPerumandla/hybrid-recommendation-system.git
cd hybrid-recommendation-system
```

### 2. Start MongoDB

Make sure MongoDB is running locally or via Atlas.

### 3. Prepare Data

Put your cleaned `interactions.csv` inside `data/processed/`.

### 4. Train Collaborative Filtering Model

```bash
python ml_pipeline/train_collab_model.py
```

This will:

* Train an SVD model using Surprise
* Save it as `cf_model.pkl`
* Dump user recommendations as JSON
* Log metrics/artifacts to MLflow

### 5. Start Backend

```bash
cd backend
uvicorn main:app --reload
```

### 6. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🔄 API Endpoints (FastAPI)

| Method | Endpoint             | Description                   |
| ------ | -------------------- | ----------------------------- |
| GET    | `/users`             | Fetch paginated list of users |
| GET    | `/likes/{user_id}`   | Posts liked by user           |
| GET    | `/recommend/content` | Content-based recs (user\_id) |
| GET    | `/recommend/collab`  | CF-based recs (user\_id)      |
| GET    | `/recommend/hybrid`  | Hybrid recs (user\_id)        |

---

## 🎯 Future Improvements

* [ ] Redis caching for frequent user queries
* [ ] Add user registration & post creation modules
* [ ] Deploy via Docker + Nginx + AWS/GCP
* [ ] Integrate TensorFlow/Keras-based image encoders

---

## 🧑‍💻 Author

Built by **Rishwanth** – Software Engineer
Connect on [LinkedIn](https://linkedin.com/in/RishwanthPerumandla) · Portfolio: [rishwanth.com](https://rishwanth.com)

---

## 📜 License

MIT License. Use freely with attribution.
