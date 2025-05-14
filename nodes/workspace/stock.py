import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import logging

# Disable logging for yfinance
logging.getLogger("yfinance").setLevel(logging.CRITICAL)

def get_sp500_tickers():
    table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    return table[0]['Symbol'].tolist()

def get_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    return stock.history(start=start_date, end=end_date)

def calculate_percentage_drop(open_price, close_price):
    return ((open_price - close_price) / open_price) * 100

def main():
    tickers = get_sp500_tickers()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    max_drop = 0
    max_drop_ticker = None
    
    for ticker in tickers:
        try:
            data = get_stock_data(ticker, start_date, end_date)
            if not data.empty:
                open_price = data.iloc[0]['Open']
                close_price = data.iloc[-1]['Close']
                drop = calculate_percentage_drop(open_price, close_price)
                
                if drop > max_drop:
                    max_drop = drop
                    max_drop_ticker = ticker
        except Exception:
            pass
    
    if max_drop_ticker:
        print(f"The stock with the largest drop is {max_drop_ticker} with a drop of {max_drop:.2f}%")
    else:
        print("No data available to determine the largest drop.")

if __name__ == "__main__":
    main()