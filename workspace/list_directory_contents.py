# filename: list_directory_contents.py
import os

directory = 'C:/projects/autogen-tutorial/stocks-chat2/coding'

# List all files in the directory
try:
    files = os.listdir(directory)
    print(f"Files in {directory}:")
    for f in files:
        print(f)
except FileNotFoundError as e:
    print(f"Directory not found: {directory}")
except Exception as e:
    print(f"An error occurred: {e}")