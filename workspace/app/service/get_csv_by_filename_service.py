# filename: app/service/get_csv_by_filename_service.py

import os

def get_csv_by_filename(filename):
    csv_directory = os.path.join('reports', 'csv')
    file_path = os.path.join(csv_directory, filename)
    try:
        if not filename.endswith('.csv'):
            return {'error': 'Invalid file format'}, 400
        with open(file_path, 'r') as file:
            content = file.readlines()
        return {'content': content}
    except FileNotFoundError:
        return {'error': 'File not found'}, 404
    except Exception as e:
        return {'error': str(e)}, 500