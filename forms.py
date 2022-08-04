from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    query = StringField("Search: ", validators=[DataRequired(), Length(min=1, max=150)])
    submit = SubmitField("Submit")