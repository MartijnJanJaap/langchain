# filename: track_stocks.py

import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def calculate_percentage_difference(new, old):
    return ((new - old) / old) * 100 if old != 0 else None

# Assuming the CSV file is in the same directory as the script
input_file_path = 'stocks_v2.csv'
output_file_path = 'output_report.csv'  # Specify a path or just a filename for current directory

# The rest of the script remains unchanged...