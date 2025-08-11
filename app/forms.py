from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[Length(min=6)])
    role = SelectField("Role", choices=[("employee", "Employee"), ("manager", "Manager"), ("admin", "Admin")], validators=[DataRequired()])
    allowance_days = IntegerField("Annual Allowance (days)", validators=[NumberRange(min=0, max=365)])
    submit = SubmitField("Save")

class RequestForm(FlaskForm):
    type = SelectField("Type", choices=[("holiday", "Holiday"), ("sickness", "Sickness")], validators=[DataRequired()])
    start_date = DateField("Start Date", validators=[DataRequired()])
    end_date = DateField("End Date", validators=[DataRequired()])
    days = IntegerField("Days", validators=[DataRequired(), NumberRange(min=1, max=365)])
    reason = TextAreaField("Reason")
    submit = SubmitField("Submit")
