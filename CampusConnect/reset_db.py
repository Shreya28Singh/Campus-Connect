import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "campus.db")

# Delete old DB if exists
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print("🗑️ Old database deleted")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Create users table
cur.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

# Insert sample users
cur.executemany("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", [
    ("admin", "admin123", "admin"),
    ("teacher1", "teach123", "teacher"),
    ("student1", "stud123", "student")
])

# Create notices table
cur.execute("""
CREATE TABLE notices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Insert sample notice
cur.execute("INSERT INTO notices (title, content) VALUES (?, ?)", 
            ("Welcome", "Welcome to CampusConnect!"))

conn.commit()
conn.close()

print("✅ Database created with tables: users, notices")
