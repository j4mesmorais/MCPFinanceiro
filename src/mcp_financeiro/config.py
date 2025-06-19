"""Application configuration loaded from a .env file."""

from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from a .env file located at the project root
load_dotenv(Path(__file__).resolve().parent.parent.parent / '.env')

# Required configuration variables
JWT_SECRET = os.getenv('JWT_SECRET')
DB_URL = os.getenv('DB_URL')

__all__ = ['JWT_SECRET', 'DB_URL']
