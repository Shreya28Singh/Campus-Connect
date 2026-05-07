# db_config.py
import os

# Get the absolute path of the project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database path (only one place to define it)
DB_PATH = os.path.join(BASE_DIR, "database", "campus.db")

print("📌 Using database at:", DB_PATH)
