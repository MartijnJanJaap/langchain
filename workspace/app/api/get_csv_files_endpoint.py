# filename: app/api/get_csv_files_endpoint.py

from flask import Flask, jsonify, request
import os

from workspace import config

app = Flask(__name__)

CSV_DIRECTORY = os.path.abspath(config.output_csv_path)

@app.route('/api/csv-files', methods=['GET'])
def get_csv_files():
    try:
        files = [f for f in os.listdir(CSV_DIRECTORY) if f.endswith('.csv')]
        print(str(files))
        return jsonify(files), 200
    except Exception as e:
        print(jsonify({'error': str(e)}))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)