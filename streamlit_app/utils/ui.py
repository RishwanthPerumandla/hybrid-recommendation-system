import streamlit as st

def show_post_card(post):
    st.image(post.get("image"), width=150)
    st.markdown(f"**Title**: {post.get('title')}")
    st.markdown(f"**Category**: {post.get('category')}")
    st.markdown(f"**Type**: {post.get('post_type')}")
    if post.get("similarity_score"):
        st.markdown(f"**Score**: `{round(post['similarity_score'], 4)}`")
    st.divider()
