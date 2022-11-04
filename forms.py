from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class SearchForm(FlaskForm):
    query = StringField("Search: ", validators=[DataRequired(), Length(min=1, max=150)])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(min=5)])
    confirm_password = PasswordField("Confirm Password: ", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Submit")