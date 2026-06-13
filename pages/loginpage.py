import streamlit as st
#from ui_utils import hide_sidebar
from auth_utils import login_user
import os
import streamlit.components.v1 as components

#hide_sidebar()

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

def show_home_html():
    html_file = os.path.join("pages", "home.html")
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=1000, scrolling=True)
    else:
        st.error("Home page HTML not found!")

if st.session_state["logged_in"]:
    show_home_html()
    st.stop()  # Stops login form from rendering below
st.title("🔐 Login")
username = st.text_input("Username or Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    user = login_user(username, password)
    if user:
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.success(f"Welcome {username}!")
        show_home_html()  # Show dashboard immediately
        st.stop()  # Stop login form from rendering
    else:
        st.error("❌ Invalid username/email or password")
