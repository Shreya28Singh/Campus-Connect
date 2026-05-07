from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
import sqlite3
from db_config import DB_PATH

import sys
import traceback

def log_uncaught_exceptions(ex_cls, ex, tb):
    with open("error.log", "w") as f:
        f.write("".join(traceback.format_exception(ex_cls, ex, tb)))

sys.excepthook = log_uncaught_exceptions


app = Flask(__name__)
app.secret_key = "supersecretkey"

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "campus.db")

print(f"✅ Using database at: {os.path.abspath(DB_PATH)}")

UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'pptx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ✅ Initialize Database

def init_db():
    """Create DB and tables if they don’t exist"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create tables if not exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        category TEXT,
        year TEXT,
        semester TEXT,
        subject TEXT,
        uploaded_by TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS notices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Insert default admin if missing
    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    ('admin', 'admin123', 'admin'))

    conn.commit()
    conn.close()
    print("✅ Database initialized")


# ✅ DB Connection
def get_db_connection():
    return sqlite3.connect(DB_PATH)

@app.route("/")
def home():
    return render_template("login.html")

# ✅ Register Page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()
        conn.close()
        
        flash("Registration successful! Please login.")
        return redirect(url_for("home"))
    
    return render_template("register.html")

# ✅ Login
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=? AND role=?", (username, password, role))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        session["username"] = username
        session["role"] = role
        return redirect(url_for("dashboard"))
    else:
        flash("Invalid credentials!")
        return redirect(url_for("home"))

# ✅ Dashboard
@app.route('/dashboard')
def dashboard():
    if "username" not in session:
        return redirect(url_for('login'))

    username = session["username"]
    role = session.get("role")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch notices
    cursor.execute("SELECT * FROM notices ORDER BY created_at DESC")
    notices = cursor.fetchall()

    conn.close()

    return render_template('dashboard.html', username=username, role=role, notices=notices)

# ✅ Upload Page
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if "username" not in session:
        return redirect(url_for("home"))
    
    if request.method == "POST":
        file = request.files["file"]
        category = request.form["category"]
        year = request.form["year"]
        semester = request.form["semester"]
        subject = request.form["subject"]
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO files (filename, category, year, semester, subject, uploaded_by) VALUES (?, ?, ?, ?, ?, ?)",
                           (filename, category, year, semester, subject, session["username"]))
            conn.commit()
            conn.close()
            
            flash("File uploaded successfully!")
            return redirect(url_for("upload"))
        else:
            flash("Invalid file type!")
    
    return render_template("upload.html")

# ✅ Download Page
@app.route("/download", methods=["GET", "POST"])
def download():
    if "username" not in session:
        return redirect(url_for("home"))
    
    files = []
    if request.method == "POST":
        category = request.form["category"]
        year = request.form["year"]
        semester = request.form["semester"]
        subject = request.form["subject"]
        
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM files WHERE category=? OR year=? OR semester=? OR subject=?"
        cursor.execute(query, (category, year, semester, subject))
        files = cursor.fetchall()
        conn.close()
    
    return render_template("download.html", files=files)

# ✅ File Download
@app.route("/files/<filename>")
def files(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# ✅ Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# ✅ Upload Notice (Admin Only)
# ✅ Notice Page (Upload + Display)
@app.route("/notice", methods=["GET", "POST"])
def upload_notice():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notices (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()

        flash("Notice posted successfully!")
        return redirect(url_for("upload_notice"))

    # fetch all notices
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notices ORDER BY id DESC")
    notices = cursor.fetchall()
    conn.close()

    return render_template("upload_notice.html", notices=notices)


# ✅ Delete Notice (Admin Only)
@app.route("/delete_notice/<int:notice_id>")
def delete_notice(notice_id):
    if "username" not in session:
        flash("Please login first!")
        return redirect(url_for("home"))

    if session.get("role") != "admin":
        flash("Access denied! Only admin can delete notices.")
        return redirect(url_for("dashboard"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notices WHERE id = ?", (notice_id,))
    conn.commit()
    conn.close()

    flash("🗑 Notice deleted successfully!")
    return redirect(url_for("dashboard"))


import webview
from threading import Thread

def run_flask():
    app.run(debug=False, port=5000)

if __name__ == "__main__":
    # Run Flask server in background
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

    # Open as desktop app
    webview.create_window("CampusConnect", "http://127.0.0.1:5000", width=2400, height=1300)
    webview.start()

if __name__ == "__main__":
    init_db()   # ✅ Always create tables if missing
    app.run(debug=True)
