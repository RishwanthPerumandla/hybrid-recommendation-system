# streamlit_app/app.py
import streamlit as st
from components.user_card import show_user_cards
from components.post_display import show_posts_grid
from api.fetch_data import get_liked_posts, get_content_recommendations, get_collab_recommendations, get_hybrid_recommendations

st.set_page_config(page_title="Post Recommender", layout="wide")
st.title("📄 Post Recommender Dashboard")

# Select user from cards
selected_user = show_user_cards()

if selected_user:
    st.markdown(f"### Selected User: `{selected_user['name']}`")
    st.markdown(f"**Email:** {selected_user['email']}  ")
    st.markdown(f"**User ID:** `{selected_user['id']}`")

    tabs = st.tabs(["Liked Posts", "Content-Based", "Collaborative", "Hybrid"])

    with tabs[0]:
        liked = get_liked_posts(selected_user['id'])
        st.subheader("❤️ Liked Posts")
        show_posts_grid(liked)

    with tabs[1]:
        cb_recs = get_content_recommendations(selected_user['id'])
        st.subheader("🤖 Content-Based Recommendations")
        show_posts_grid(cb_recs)

    with tabs[2]:
        cf_recs = get_collab_recommendations(selected_user['id'])
        st.subheader("🧠 Collaborative Filtering Recommendations")
        show_posts_grid(cf_recs)

    with tabs[3]:
        hybrid_recs = get_hybrid_recommendations(selected_user['id'])
        st.subheader("🌀 Hybrid Recommendations")
        show_posts_grid(hybrid_recs)
else:
    st.warning("Please select a user to view recommendations.")
