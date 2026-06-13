import streamlit as st
#from ui_utils import hide_sidebar
from auth_utils import login_user

#hide_sidebar()

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Already logged in → dashboard
if st.session_state["logged_in"]:
    st.switch_page("pages/dashboard.py")

st.title("🔐 Login")

username = st.text_input("Username or Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if login_user(username, password):
        st.session_state["logged_in"] = True
        st.switch_page("pages/dashboard.py")
    else:
        st.error("❌ Invalid credentials")
