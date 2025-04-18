import streamlit as st

if "username" in st.session_state:
    st.switch_page("pages/profile.py")
else:
    st.switch_page("pages/home.py")
