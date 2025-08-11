from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from pathlib import Path
import os

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "sqlite:///" + str(Path(app.instance_path) / "app.db")),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # Ensure instance folder exists
    try:
        Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    except OSError:
        pass

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = "auth.login"

    from .models import User, Role, Request
    from .routes import main_bp
    from .auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app

def seed_data():
    from .models import User, Role
    from werkzeug.security import generate_password_hash
    if not Role.query.first():
        admin = Role(name="admin")
        manager = Role(name="manager")
        employee = Role(name="employee")
        db.session.add_all([admin, manager, employee])
        db.session.commit()
    if not User.query.filter_by(email="admin@example.com").first():
        admin_role = Role.query.filter_by(name="admin").first()
        u = User(
            name="Admin User",
            email="admin@example.com",
            role=admin_role,
            allowance_days=28
        )
        u.password_hash = generate_password_hash("admin123")
        db.session.add(u)
        db.session.commit()
