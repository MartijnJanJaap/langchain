# filename: app/service/get_csv_files_service.py

import os

def get_csv_files():
    csv_directory = os.path.join('reports', 'csv')
    try:
        files = os.listdir(csv_directory)
        csv_files = [file for file in files if file.endswith('.csv')]
        return csv_files
    except FileNotFoundError:
        return []