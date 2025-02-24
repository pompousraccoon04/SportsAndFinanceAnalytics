import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Fetch AAPL data explicitly
stock = yf.download("AAPL", start="2023-01-01", end="2025-02-23", progress=False)

# Debug: Confirm columns
print("Columns:", stock.columns.tolist())
print("First 5 rows:")
print(stock.head())

# Use 'Close' (confirmed present)
stock["Daily_Return"] = stock["Close"].pct_change() * 100
stock["MA50"] = stock["Close"].rolling(window=50).mean()

# Stats
avg_return = stock["Daily_Return"].mean()
volatility = stock["Daily_Return"].std()
print(f"Average Daily Return: {avg_return:.2f}%")
print(f"Volatility (Std Dev): {volatility:.2f}%")

# Plot price trend
plt.figure(figsize=(12, 6))
plt.plot(stock["Close"], label="Close Price", color="blue")
plt.plot(stock["MA50"], label="50-Day MA", color="orange")
plt.title("AAPL Stock Price Trend (2023-2025)")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.savefig("aapl_price_trend.png")
plt.show()

# Plot returns histogram
plt.figure(figsize=(10, 6))
stock["Daily_Return"].hist(bins=50, color="green", alpha=0.7)
plt.title("AAPL Daily Returns Distribution (2023-2025)")
plt.xlabel("Daily Return (%)")
plt.ylabel("Frequency")
plt.savefig("aapl_returns_hist.png")
plt.show()