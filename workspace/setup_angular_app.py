# filename: setup_angular_app.py
import subprocess
import os

def install_node_and_angular():
    try:
        # Check if Node.js is installed
        subprocess.run(["node", "-v"], check=True)
        print("Node.js is already installed.")
    except subprocess.CalledProcessError:
        # Download and install Node.js
        print("Node.js is not installed. Please install it manually.")
        return

    try:
        # Check if npm is installed
        subprocess.run(["npm", "-v"], check=True)
        print("npm is already installed.")
    except subprocess.CalledProcessError:
        print("npm is not installed. Please install Node.js to get npm.")
        return

    try:
        # Check if Angular CLI is installed
        subprocess.run(["ng", "version"], check=True)
        print("Angular CLI is already installed.")
    except subprocess.CalledProcessError:
        print("Installing Angular CLI...")
        subprocess.run(["npm", "install", "-g", "@angular/cli"], check=True)
    else:
        print("Angular CLI installation encountered an issue.")

def create_angular_project():
    # Create a new Angular app if it doesn't already exist
    if not os.path.exists("angular-csv-viewer"):
        print("Creating a new Angular project...")
        subprocess.run(["ng", "new", "angular-csv-viewer", "--skip-git", "--style=css", "--routing"], check=True)
        print("Angular project created.")
    else:
        print("Angular project already exists.")

def generate_angular_app():
    print("Generating Angular components...")
    os.chdir("angular-csv-viewer")

    # Generate Angular components
    subprocess.run(["ng", "generate", "component", "csv-viewer"], check=True)
    subprocess.run(["ng", "generate", "component", "csv-table"], check=True)
    
    # Serve the Angular app
    print("Running Angular development server...")
    subprocess.run(["npm", "install"], check=True)
    subprocess.run(["npm", "start"], check=True)

if __name__ == "__main__":
    install_node_and_angular()
    create_angular_project()
    generate_angular_app()