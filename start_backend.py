import os
import sys
import subprocess
from pathlib import Path

def install_requirements():
    """Install Python requirements for the backend."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Backend dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f" Error installing requirements: {e}")
        return False

if __name__ == "__main__":
    print("🏗Setting up FloorPlan AI Backend...")
    
    # Install requirements
    if not install_requirements():
        print(" Failed to install requirements")
        sys.exit(1)
    
    print("Starting FloorPlan AI backend server...")
    os.system("gunicorn -c gunicorn_config.py app.main:app")
