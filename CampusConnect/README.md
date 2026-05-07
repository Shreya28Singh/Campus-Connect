# Campus Connect Desktop App

## Overview
Campus Connect is a desktop application designed for students to easily access academic resources.  
It includes a login system, dashboard, and local SQLite database support.  
The app uses **Python, Flask, SQLite**, and **PyWebview**, running as a standalone desktop application on Windows.

---

## Features
- User login system  
- Dashboard to access academic resources  
- Native desktop window (no browser needed)  
- Fully functional with SQLite database  
- Offline usage supported  

---

## System Requirements
- Windows 10 or higher (64-bit recommended)  
- Microsoft Visual C++ Redistributable (x64) installed:  
[Download VC++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)  

> Python is **not required** for users since the app is packaged as a standalone `.exe`.

---

## Installation
1. Extract the ZIP folder `CampusConnectApp.zip` to any location.  
2. Ensure the following files/folders are present inside:

CampusConnectApp/
├─ app.exe
├─ database.db
└─ README.md


3. Double-click `app.exe` to run the application.  

> The app will open in a native desktop window using PyWebview.

---

## Usage
1. Open `app.exe`.  
2. Login with your username and password.  
3. Navigate through the dashboard to access resources.  
4. Changes are automatically saved in `database.db`.

---

## Database Notes
- The app uses `database.db` (SQLite) to store user and resource data.  
- If the database is missing, the app can be configured to auto-create it (optional enhancement).  

---

## Troubleshooting
- App does not open → make sure **VC++ Redistributable** is installed.  
- Antivirus may block the `.exe` → temporarily allow or unblock the file.  
- Database issues → ensure `database.db` is in the same folder as `app.exe`.

---

## Distribution
- Share the **entire folder or ZIP**, not just the `.exe`.  
- Ensure `database.db` is included for proper functionality.  

---

## Contact / Support
**Developer:** Shreya Singh  
**Email:** shreya.singh23@tnu.in
