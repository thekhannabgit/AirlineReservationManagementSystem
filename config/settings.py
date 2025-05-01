# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = "sqlite:///database/skylink_db.sqlite"
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRY_MINUTES = 30