import streamlit as st
from auth_utils import register_user

st.title("Signup")

username = st.text_input("Username")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Create Account"):
    if username and email and password:
        register_user(username, email, password)
        st.success("Account created successfully!! Go back and login through the home page")
    else:
        st.error("All fields are required")
import streamlit as st
#from ui_utils import hide_sidebar

#hide_sidebar()

