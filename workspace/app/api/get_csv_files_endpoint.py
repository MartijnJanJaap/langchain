# filename: app/api/get_csv_files_endpoint.py

from flask import Flask, jsonify

from workspace.app.service.get_csv_files_service import get_csv_files

app = Flask(__name__)

@app.route('/api/csv-files', methods=['GET'])
def get_csv_files_endpoint():
    csv_files = get_csv_files()
    return jsonify({'csv_files': csv_files})

if __name__ == '__main__':
    app.run(debug=True)