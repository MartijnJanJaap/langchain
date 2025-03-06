# filename: stock_tracker.py
from datetime import datetime
import pandas as pd
import yfinance as yf
import os
import generate_csv_report as htmlGenerator

def fetch_stock_data(ticker, period):
    stock = yf.Ticker(ticker)
    return stock.history(period=period)

def calculate_percentage_difference(old_price, new_price):
    if pd.isna(old_price) or pd.isna(new_price) or old_price == 0:
        return "NAN"
    return ((new_price - old_price) / old_price) * 100

def main():
    # Print current working directory
    print(f"Current Working Directory: {os.getcwd()}")

    # Use the correct file name
    input_file = 'C:/projects/autogen-tutorial/stocks-chat2/coding/stocks_v2.csv'
    output_file = 'stock_report_' + datetime.now().strftime('%Y-%m-%d') + '.csv'

    df = pd.read_csv(input_file, header=None, names=["Ticker", "Company", "Industry", "Country"])

    results = []

    for index, row in df.iterrows():
        ticker = row['Ticker']
        print("processing " + ticker)
        
        try:
            daily_data = fetch_stock_data(ticker, '5d')
            weekly_data = fetch_stock_data(ticker, '7d')
            monthly_data = fetch_stock_data(ticker, '1mo')
            
            if daily_data.empty or weekly_data.empty or monthly_data.empty:
                raise ValueError(f"{ticker}: possibly delisted; no price data found")

            daily_change = (
                calculate_percentage_difference(daily_data['Close'].iloc[-2], daily_data['Close'].iloc[-1])
                if len(daily_data) >= 2 else "NAN"
            )
            weekly_change = (
                calculate_percentage_difference(weekly_data['Close'].iloc[0], weekly_data['Close'].iloc[-1])
                if len(weekly_data) >= 2 else "NAN"
            )
            monthly_change = (
                calculate_percentage_difference(monthly_data['Close'].iloc[0], monthly_data['Close'].iloc[-1])
                if len(monthly_data) >= 2 else "NAN"
            )
            
            results.append({
                "Ticker": row['Ticker'],
                "Company": row['Company'],
                "Industry": row['Industry'],
                "Country": row['Country'],
                "Daily Change (%)": daily_change,
                "Weekly Change (%)": weekly_change,
                "Monthly Change (%)": monthly_change
            })
        except Exception as e:
            print(f"Error processing ticker {ticker}: {e}")
            results.append({
                "Ticker": row['Ticker'],
                "Company": row['Company'],
                "Industry": row['Industry'],
                "Country": row['Country'],
                "Daily Change (%)": "NAN",
                "Weekly Change (%)": "NAN",
                "Monthly Change (%)": "NAN"
            })

    report_df = pd.DataFrame(results)
    report_df.to_csv(output_file, index=False)
    print(f"Report generated: {output_file}")
    htmlGenerator.generate_html()

if __name__ == "__main__":
    main()