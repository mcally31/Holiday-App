@echo off
setlocal
REM Create venv if not exists
if not exist venv (
  py -m venv venv
)
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

set FLASK_APP=app
set FLASK_RUN_PORT=5000
python -c "from app import db, create_app, seed_data; app=create_app(); ctx=app.app_context(); ctx.push(); db.create_all(); seed_data(); print('Database ready.')" 

flask --app app run --debug
