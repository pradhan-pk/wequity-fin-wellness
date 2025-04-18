import streamlit as st
import requests

st.set_page_config(page_title="Login", page_icon="🔐")

st.title("🔐 Login to Your Profile")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if not username or not password:
        st.warning("Please enter both username and password.")
    else:
        response = requests.post("http://localhost:8000/login", json={
            "username": username,
            "password": password
        })
        if response.status_code == 200:
            st.success("Login successful!")
            st.session_state["username"] = username
            st.switch_page("pages/profile.py")
        else:
            st.error("Invalid credentials.")
