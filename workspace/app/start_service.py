# filename: app/start_service.py

import os
from workspace.app.api.get_csv_files_endpoint import app

def main():
    # Set the environment variable for Flask
    os.environ['FLASK_APP'] = 'app/api/get_csv_files_endpoint'
    
    # Enable debug mode
    app.config['DEBUG'] = True

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()