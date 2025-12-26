import streamlit as st
import pandas as pd
import numpy as np
from pycoingecko import CoinGeckoAPI
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
st.set_page_config(
    page_title="Crypto Risk Dashboard (CoinGecko)",
    layout="wide"
)
st.title("📊 Crypto Risk & Return Dashboard (CoinGecko – Free API)")

cg = CoinGeckoAPI()

CRYPTO_MAP = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Solana": "solana"
}

@st.cache_data(show_spinner=True)
def fetch_coingecko_data(coin_id):
    """
    CoinGecko Free API allows ONLY last 365 days
    """
    data = cg.get_coin_market_chart_by_id(
        id=coin_id,
        vs_currency="usd",
        days=365
    )

    df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    df["Return"] = df["price"].pct_change()
    df["Volatility"] = df["Return"].rolling(30, min_periods=5).std()

    return df.dropna()
st.sidebar.header("🔧 Controls")

# Multi-select slicer
selected_cryptos = st.sidebar.multiselect(
    "Select Cryptocurrencies",
    options=list(CRYPTO_MAP.keys()),
    default=list(CRYPTO_MAP.keys())
)

if not selected_cryptos:
    st.warning("Please select at least one cryptocurrency.")
    st.stop()

focus_crypto = st.sidebar.radio(
    "Price & Volatility Chart",
    options=selected_cryptos
)

st.sidebar.subheader("📅 Date Range (Max 1 Year)")

today = datetime.today().date()
min_date = today - timedelta(days=365)

start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    value=(today - timedelta(days=180), today),
    min_value=min_date,
    max_value=today
)

if start_date >= end_date:
    st.error("Start date must be before end date.")
    st.stop()

raw_data = {
    crypto: fetch_coingecko_data(CRYPTO_MAP[crypto])
    for crypto in selected_cryptos
}
data = {
    crypto: df.loc[start_date:end_date]
    for crypto, df in raw_data.items()
}

st.subheader(f"📈 Price & Volatility — {focus_crypto}")

df_focus = data[focus_crypto]

fig_price = go.Figure()

fig_price.add_trace(go.Scatter(
    x=df_focus.index,
    y=df_focus["price"],
    name="Price"
))

fig_price.add_trace(go.Scatter(
    x=df_focus.index,
    y=df_focus["Volatility"],
    name="Volatility",
    yaxis="y2"
))

fig_price.update_layout(
    xaxis_title="Date",
    yaxis=dict(title="Price (USD)"),
    yaxis2=dict(
        title="Volatility",
        overlaying="y",
        side="right",
        showgrid=False
    ),
    legend=dict(orientation="h")
)

st.plotly_chart(fig_price, use_container_width=True)

metrics = []

for crypto, df in data.items():
    mean_return = df["Return"].mean()
    volatility = df["Return"].std()
    sharpe = (mean_return / volatility) * np.sqrt(252) if volatility != 0 else 0

    metrics.append({
        "Crypto": crypto,
        "Avg Daily Return": mean_return,
        "Volatility": volatility,
        "Sharpe Ratio": sharpe
    })

metrics_df = pd.DataFrame(metrics)
metrics_df["SharpeAbs"] = metrics_df["Sharpe Ratio"].abs()

st.subheader("📌 Key Risk Metrics")

cols = st.columns(len(metrics_df))
for col, row in zip(cols, metrics_df.itertuples()):
    col.metric(
        label=row.Crypto,
        value=f"Sharpe {row._4:.2f}",
        delta=f"Volatility {row.Volatility:.4f}"
    )
st.subheader("⚖️ Risk vs Return")

fig_scatter = px.scatter(
    metrics_df,
    x="Volatility",
    y="Avg Daily Return",
    size="SharpeAbs",
    text="Crypto",
    title="Risk vs Return (Last 365 Days)"
)

fig_scatter.update_traces(textposition="top center")

st.plotly_chart(fig_scatter, use_container_width=True)
st.subheader("📊 Risk Metrics Table")
st.dataframe(metrics_df)
