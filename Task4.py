import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Risk Classification Dashboard",
    layout="wide"
)

# ---------------- Custom CSS ----------------
st.markdown("""
<style>
body { background-color: #0b1023; }
.main { background-color: #0b1023; color: white; }
.card {
    padding: 15px;
    border-radius: 12px;
    color: white;
    height: 160px;
}
.high { background-color: #4b1e2f; border: 1px solid #ff4d6d; }
.medium { background-color: #4a3b1b; border: 1px solid #f5c542; }
.low { background-color: #1f3b2d; border: 1px solid #4ade80; }
.metric-box {
    background-color: #141a3a;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Fetch Live Crypto Data ----------------
@st.cache_data(ttl=3600)
def fetch_crypto_data(coin_id, days=30):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": days}

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            return None

        data = response.json()
        prices = pd.DataFrame(data.get("prices", []), columns=["timestamp", "price"])

        if prices.empty:
            return None

        prices["price"] = prices["price"].astype(float)
        prices["returns"] = prices["price"].pct_change()

        volatility = prices["returns"].std() * 100
        return round(volatility, 2)

    except Exception:
        return None

# ---------------- Crypto Assets ----------------
coins = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Solana": "solana",
    "Cardano": "cardano",
    "Dogecoin": "dogecoin"
}

# ---------------- Build Volatility Table ----------------
records = []

for name, cid in coins.items():
    vol = fetch_crypto_data(cid)
    if vol is not None:
        records.append([name, vol])

df = pd.DataFrame(records, columns=["Asset", "Volatility (%)"])

if df.empty:
    st.error("⚠️ Unable to fetch crypto data. Please try again later.")
    st.stop()


# ---------------- Guaranteed Risk Segregation ----------------
df = df.sort_values("Volatility (%)").reset_index(drop=True)

n = len(df)

def assign_risk(index):
    if index < n / 3:
        return "Low"
    elif index < 2 * n / 3:
        return "Medium"
    else:
        return "High"

df["Risk"] = df.index.map(assign_risk)


# ---------------- Title ----------------
st.markdown("## 🚀 **Milestone 4: Risk Classification & Reporting**")
left, right = st.columns([1, 2])

# ---------------- Left Panel ----------------
with left:
    st.markdown("### 📌 Requirements")
    st.markdown("""
    - Live volatility-based thresholds  
    - Dynamic risk segregation  
    - Visual highlighting  
    - Exportable reports  
    """)

    st.markdown("### ✅ Project Status")
    st.progress(100)
    st.caption("Milestone 1 → 4 Completed")

# ---------------- Right Panel ----------------
with right:
    st.markdown("## 📊 Risk Classification Dashboard")
    st.caption("Live Crypto Volatility Analysis")

    # ---------------- Risk Cards ----------------
    c1, c2, c3 = st.columns(3)

    def render_card(risk):
        subset = df[df["Risk"] == risk]
        if subset.empty:
            return "<p>None</p>"
        return "".join(
            f"<p>{row.Asset} <b>{row['Volatility (%)']}%</b></p>"
            for _, row in subset.iterrows()
        )

    with c1:
        st.markdown(f"""
        <div class="card high">
            <h4>🔴 High Risk</h4>
            {render_card("High")}
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card medium">
            <h4>🟡 Medium Risk</h4>
            {render_card("Medium")}
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="card low">
            <h4>🟢 Low Risk</h4>
            {render_card("Low")}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ---------------- Summary & Chart ----------------
    s1, s2 = st.columns([1.3, 1])

    with s1:
        st.markdown("### 📑 Risk Summary Report")
        st.markdown(f"""
        <div class="metric-box">
            <p>Total Cryptocurrencies: <b>{len(df)}</b></p>
            <p>Average Volatility: <b>{round(df['Volatility (%)'].mean(), 2)}%</b></p>
            <p>Risk Distribution:
                <b>
                {len(df[df.Risk=='High'])} High /
                {len(df[df.Risk=='Medium'])} Medium /
                {len(df[df.Risk=='Low'])} Low
                </b>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.download_button(
            "⬇️ Download CSV",
            df.to_csv(index=False),
            file_name="live_crypto_risk_report.csv"
        )

    with s2:
        chart_df = df["Risk"].value_counts().reset_index()
        chart_df.columns = ["Risk Level", "Count"]

        fig = px.pie(
            chart_df,
            values="Count",
            names="Risk Level",
            hole=0.65,
            color="Risk Level",
            color_discrete_map={
                "High": "#ff4d6d",
                "Medium": "#f5c542",
                "Low": "#4ade80"
            }
        )

        fig.update_layout(
            height=260,
            width=260,
            paper_bgcolor="#141a3a",
            font_color="white",
            margin=dict(t=20, b=20, l=20, r=20)
        )

        st.plotly_chart(fig, use_container_width=False)
