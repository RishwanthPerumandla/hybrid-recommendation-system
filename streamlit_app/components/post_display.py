# streamlit_app/components/post_display.py
import streamlit as st

def show_posts_grid(posts):
    if not posts:
        st.info("No posts to display.")
        return

    cols = st.columns(3)
    for i, post in enumerate(posts):
        with cols[i % 3]:
            st.image(post.get("image"), use_column_width=True)
            st.markdown(f"**{post.get('title', 'No Title')}**")
            st.markdown(f"Category: `{post.get('category', 'N/A')}`")
            st.markdown(f"Type: `{post.get('post_type', 'N/A')}`")
            if "similarity_score" in post:
                st.markdown(f"Similarity: `{post['similarity_score']}`")
            if "matched_reason" in post:
                st.caption(post["matched_reason"])
