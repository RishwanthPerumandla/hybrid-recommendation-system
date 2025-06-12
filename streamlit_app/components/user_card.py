# streamlit_app/components/user_card.py
import streamlit as st
import requests

def fetch_users():
    response = requests.get("http://localhost:8000/users")
    if response.status_code == 200:
        print(response)
        return response.json().get("users", [])
    return []

def show_user_cards():
    users = fetch_users()
    if not users:
        st.error("⚠️ No users found.")
        return None

    selected_user = None
    cols = st.columns(3)

    for i, user in enumerate(users):
        with cols[i % 3]:
            if st.button(f"👤 {user['name']}", key=user['id']):
                st.session_state.selected_user = user

    return st.session_state.get("selected_user")
