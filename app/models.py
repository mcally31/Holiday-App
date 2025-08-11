from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    users = db.relationship("User", back_populates="role")

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)
    role = db.relationship("Role", back_populates="users")
    allowance_days = db.Column(db.Integer, default=28)
    days_taken = db.Column(db.Integer, default=0)

    requests = db.relationship("Request", back_populates="user", cascade="all, delete-orphan")

    @property
    def is_admin(self):
        return self.role and self.role.name == "admin"

    @property
    def is_manager(self):
        return self.role and self.role.name == "manager"

    @property
    def is_employee(self):
        return self.role and self.role.name == "employee"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="requests")
    type = db.Column(db.String(20), nullable=False)  # holiday or sickness
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    days = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default="pending")  # pending/approved/declined
    manager_comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
