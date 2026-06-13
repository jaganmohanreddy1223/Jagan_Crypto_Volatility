import streamlit as st

st.set_page_config(
    page_title="Data Acquisition",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🔒 Hide sidebar completely
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="stSidebarNav"] {
            display: none;
        }
        header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# 🔐 Login protection
if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

st.title("🚀 Data Acquisition")

html_path = Path("html/milestone1.html")
components.html(
    html_path.read_text(encoding="utf-8"),
    height=1200,
    scrolling=True
)
