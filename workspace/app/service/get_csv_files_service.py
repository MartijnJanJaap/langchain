# filename: app/service/get_csv_files_service.py
import os

from workspace import config

def get_csv_files():
    csv_directory = os.path.abspath(config.output_csv_path)
    try:
        print("1")
        files = os.listdir(csv_directory)
        print("2")
        csv_files = [file for file in files if file.endswith('.csv')]
        print("3 " + str(csv_files))
        return csv_files
    except FileNotFoundError:
        return []