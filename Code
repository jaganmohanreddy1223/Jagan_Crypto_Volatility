import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
 
import streamlit as st
 
data = pd.read_csv('crypto_prices.csv')
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

print(data.head())

data['Return'] = data['Close'].pct_change()

daily_volatility = data['Return'].std()
annual_volatility = daily_volatility * np.sqrt(252)  # Annualized
print(f"Daily Volatility: {daily_volatility:.4f}")
print(f"Annual Volatility: {annual_volatility:.4f}")

confidence_level = 0.05  # 5% worst-case scenario
VaR = data['Return'].quantile(confidence_level)
print(f"Value at Risk (5% confidence): {VaR:.4f}")

plt.figure(figsize=(12,6))
plt.plot(data.index, data['Close'], label='Close Price')
plt.title('Crypto Price Trend')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()
 
plt.figure(figsize=(12,6))
sns.histplot(data['Return'].dropna(), bins=50, kde=True)
plt.title('Return Distribution')
plt.xlabel('Daily Return')
plt.show()
 
plt.figure(figsize=(12,6))
data['Return'].dropna().cumsum().plot()
plt.title('Cumulative Returns')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.show()

data.to_csv('crypto_analysis_results.csv')



import yfinance as yf
btc = yf.Ticker("BTC-USD")
data = btc.history(period="1y")
print(data.head())
