from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from . import db
from .models import User, Role, Request as LeaveRequest
from .forms import UserForm, RequestForm

main_bp = Blueprint("main", __name__)

def role_required(role_name):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))
            if role_name == "admin" and not current_user.is_admin:
                flash("Admins only.", "warning")
                return redirect(url_for("main.dashboard"))
            if role_name == "manager" and not (current_user.is_manager or current_user.is_admin):
                flash("Managers only.", "warning")
                return redirect(url_for("main.dashboard"))
            return fn(*args, **kwargs)
        wrapper.__name__ = fn.__name__
        return wrapper
    return decorator

@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))

@main_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.is_admin:
        users = User.query.all()
        pending = LeaveRequest.query.filter_by(status="pending").all()
        return render_template("dashboard_admin.html", users=users, pending=pending)
    elif current_user.is_manager:
        pending = LeaveRequest.query.filter_by(status="pending").all()
        return render_template("dashboard_manager.html", pending=pending)
    else:
        # employee
        my_reqs = LeaveRequest.query.filter_by(user_id=current_user.id).order_by(LeaveRequest.created_at.desc()).all()
        return render_template("dashboard_employee.html", my_reqs=my_reqs)

@main_bp.route("/users/new", methods=["GET", "POST"])
@login_required
@role_required("admin")
def users_new():
    form = UserForm()
    if form.validate_on_submit():
        role = Role.query.filter_by(name=form.role.data).first()
        u = User(
            name=form.name.data.strip(),
            email=form.email.data.lower(),
            role=role,
            allowance_days=form.allowance_days.data or 28
        )
        if form.password.data:
            u.password_hash = generate_password_hash(form.password.data)
        else:
            u.password_hash = generate_password_hash("changeme123")
        db.session.add(u)
        db.session.commit()
        flash("User created", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("users_new.html", form=form)

@main_bp.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin")
def users_edit(user_id):
    u = User.query.get_or_404(user_id)
    form = UserForm(obj=u)
    if form.validate_on_submit():
        u.name = form.name.data.strip()
        u.email = form.email.data.lower()
        role = Role.query.filter_by(name=form.role.data).first()
        u.role = role
        u.allowance_days = form.allowance_days.data or u.allowance_days
        if form.password.data:
            u.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        flash("User updated", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("users_edit.html", form=form, user=u)

@main_bp.route("/request/new", methods=["GET", "POST"])
@login_required
def request_new():
    form = RequestForm()
    if form.validate_on_submit():
        r = LeaveRequest(
            user_id=current_user.id,
            type=form.type.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            days=form.days.data,
            reason=form.reason.data.strip() if form.reason.data else ""
        )
        db.session.add(r)
        db.session.commit()
        flash("Request submitted", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("request_new.html", form=form)

@main_bp.route("/requests/<int:req_id>/approve", methods=["POST"])
@login_required
@role_required("manager")
def approve_request(req_id):
    r = LeaveRequest.query.get_or_404(req_id)
    r.status = "approved"
    r.manager_comment = request.form.get("manager_comment", "")
    # Update user's days_taken only for holidays
    if r.type == "holiday":
        r.user.days_taken = (r.user.days_taken or 0) + (r.days or 0)
    db.session.commit()
    flash("Request approved", "success")
    return redirect(url_for("main.dashboard"))

@main_bp.route("/requests/<int:req_id>/decline", methods=["POST"])
@login_required
@role_required("manager")
def decline_request(req_id):
    r = LeaveRequest.query.get_or_404(req_id)
    r.status = "declined"
    r.manager_comment = request.form.get("manager_comment", "")
    db.session.commit()
    flash("Request declined", "info")
    return redirect(url_for("main.dashboard"))
