# Holiday & Sickness Tracker — MVP (Flask + SQLite)

This is a simple, self-contained web app you can run on your computer. It lets employees request holiday/sickness, managers approve/decline, and admins manage users.

## Quick Start (Windows)
1) Install Python 3.10+ from https://www.python.org (if you don't already have it)
2) Double-click `start.bat` (or right-click → Open). The first run will install dependencies and create the database.
3) When you see "Running on http://127.0.0.1:5000", open that link in your browser.
4) Log in with:
   - **Admin:** `admin@example.com` / `admin123`

## Quick Start (Mac/Linux)
1) Ensure Python 3.10+ is installed (`python3 --version`).
2) In Terminal: `chmod +x start_mac.sh && ./start_mac.sh`
3) Open the link shown (usually http://127.0.0.1:5000).

## Roles
- **Admin:** manage users, set roles (admin/manager/employee)
- **Manager:** approve/decline requests from their team
- **Employee:** submit and view requests

## Features
- Login/logout
- Create employees/managers/admins
- Submit holiday/sickness with dates, type, reason
- Manager approval flow + comments
- Simple dashboards
- Basic allowance tracking (annual allowance with days taken/remaining)
- SQLite database file stored in `instance/app.db`

## Notes
- This is an MVP for local use. For production (cloud hosting, multi-user access), you’ll want to add email, audit logs, file storage, and deploy to a host like Render/Fly/Heroku/etc.
- Change `SECRET_KEY` in `.env` before using with real data.
