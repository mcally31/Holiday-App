#!/usr/bin/env bash
set -e
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

export FLASK_APP=app
export FLASK_RUN_PORT=5000
python3 -c "from app import db, create_app, seed_data; app=create_app(); app.app_context().push(); db.create_all(); seed_data(); print('Database ready.')"

flask --app app run --debug
