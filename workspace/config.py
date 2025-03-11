# filename: config.py
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

input_file_path = PROJECT_ROOT / 'init/stocks.csv'
output_csv_path = PROJECT_ROOT / 'reports/csv/'
output_html_path = 'reports/view.html'

