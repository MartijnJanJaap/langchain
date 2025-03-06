# filename: test_ticker_data.py

import yfinance as yf

def test_ticker(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period='5d')
    if data.empty:
        print(f"{ticker}: no price data found")
    else:
        print(f"{ticker}: data retrieved successfully")
        print(data)

test_ticker("AAPL")  # You can replace "AAPL" with any other ticker to test