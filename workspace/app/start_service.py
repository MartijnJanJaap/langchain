# filename: app/start_service.py

import os
from workspace.app.api.get_csv_files_endpoint import app
from flask_cors import CORS

def main():
    # Set the environment variable for Flask

    CORS(app, resources={r"/*": {"origins": "http://localhost:56477"}})

    os.environ['FLASK_APP'] = 'app/api/get_csv_files_endpoint'
    
    # Enable debug mode
    app.config['DEBUG'] = True

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()