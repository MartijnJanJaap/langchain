# filename: app/api/get_csv_by_filename.py

from flask import Flask, jsonify, request

from workspace.app.service.get_csv_by_filename_service import get_csv_by_filename

app = Flask(__name__)

@app.route('/api/csv-file', methods=['GET'])
def get_csv_by_filename_endpoint():
    filename = request.args.get('filename')
    if not filename:
        return jsonify({'error': 'Filename parameter is required'}), 400

    result, status_code = get_csv_by_filename(filename)
    return jsonify(result), status_code

if __name__ == '__main__':
    app.run(debug=True)