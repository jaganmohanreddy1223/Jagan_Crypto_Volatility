import streamlit as st

st.set_page_config(
    page_title="Dashboard",
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
import os

st.set_page_config(page_title="Dashboard", layout="wide")

# 🔐 Block direct access
if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

# ---------- STREAMLIT BUTTONS (REAL NAVIGATION) ----------
st.markdown("## 🚀 Workflow Modules")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📊 Data Acquisition", use_container_width=True):
        st.switch_page("pages/DataAquisition.py")

with col2:
    if st.button("📈 Data Pre-Processing", use_container_width=True):
        st.switch_page("pages/Data_Pre_Processing.py")

with col3:
    if st.button("📉 Risk Metrics", use_container_width=True):
        st.switch_page("pages/Data_Analysis.py")

with col4:
    if st.button("📑 Risk Classification", use_container_width=True):
        st.switch_page("pages/Data_Reporting.py")

# ---------- Load HTML ----------
def show_home_html():
    base_dir = os.path.dirname(__file__)
    root_dir = os.path.abspath(os.path.join(base_dir, ".."))
    html_path = os.path.join(root_dir, "html", "home.html")

    with open(html_path, "r", encoding="utf-8") as f:
        components.html(f.read(), height=650, scrolling=False)

show_home_html()


