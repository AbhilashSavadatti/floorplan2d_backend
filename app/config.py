import os
from pathlib import Path

# Base directory of the backend
BASE_DIR = Path(__file__).resolve().parent.parent

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class Config:
    """Application configuration."""
    UPLOAD_FOLDER = UPLOAD_FOLDER
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    MODEL_PATH = os.path.join(BASE_DIR, 'best.pt')

# Create an instance of Config
config = Config()