!pip install fpdf
import pandas as pd
import numpy as np
import plotly.express as px
from fpdf import FPDF
data = {
    "Asset": ["BTC", "ETH", "XRP", "ADA", "SOL", "BNB", "DOT", "LTC"],
    "Volatility (%)": [85, 72, 45, 38, 65, 30, 42, 28]
}

df = pd.DataFrame(data)
HIGH_RISK_THRESHOLD = 60
MEDIUM_RISK_THRESHOLD = 35
def classify_risk(volatility):
    if volatility >= HIGH_RISK_THRESHOLD:
        return "High Risk"
    elif volatility >= MEDIUM_RISK_THRESHOLD:
        return "Medium Risk"
    else:
        return "Low Risk"

df["Risk Level"] = df["Volatility (%)"].apply(classify_risk)
assert df["Risk Level"].isnull().sum() == 0, "Risk classification failed!"
bar_chart = px.bar(
    df,
    x="Asset",
    y="Volatility (%)",
    color="Risk Level",
    title="Asset Risk Classification Dashboard",
    color_discrete_map={
        "High Risk": "red",
        "Medium Risk": "orange",
        "Low Risk": "green"
    }
)

bar_chart.show()
total_assets = len(df)
average_volatility = round(df["Volatility (%)"].mean(), 2)

risk_distribution = (
    df["Risk Level"]
    .value_counts()
    .reset_index()
)

risk_distribution.columns = ["Risk Level", "Asset Count"]
donut_chart = px.pie(
    risk_distribution,
    values="Asset Count",
    names="Risk Level",
    hole=0.5,
    title="Risk Distribution Across Assets",
    color="Risk Level",
    color_discrete_map={
        "High Risk": "red",
        "Medium Risk": "orange",
        "Low Risk": "green"
    }
)

donut_chart.show()
summary_report = pd.DataFrame({
    "Metric": [
        "Total Assets Analyzed",
        "Average Volatility (%)"
    ],
    "Value": [
        total_assets,
        average_volatility
    ]
})
print(summary_report)
