# config/config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = os.path.join(BASE_DIR, "..", "database", "airline.db")
