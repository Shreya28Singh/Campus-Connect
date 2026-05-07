import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "campus.db")

print("📌 Checking database at:", DB_PATH)

if not os.path.exists(DB_PATH):
    print("❌ Database file does NOT exist!")
    exit()

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# List all tables
print("\n📋 Tables in DB:")
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()
if not tables:
    print("❌ No tables found!")
else:
    for t in tables:
        print("   -", t[0])

# Check users table
try:
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    print("\n👤 Users table contents:")
    for u in users:
        print(u)
except Exception as e:
    print("\n⚠️ Users table check failed:", e)

# Check notices table
try:
    cur.execute("SELECT * FROM notices;")
    notices = cur.fetchall()
    print("\n📢 Notices table contents:")
    for n in notices:
        print(n)
except Exception as e:
    print("\n⚠️ Notices table check failed:", e)

conn.close()
