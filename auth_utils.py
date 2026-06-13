import streamlit as st

USERS = {
    "admin": "admin123",
    "jagan": "crypto123"
}

def login_user(username, password):
    username = username.strip()
    password = password.strip()

    if username in USERS and USERS[username] == password:
        return username
    return None