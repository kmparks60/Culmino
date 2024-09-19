from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo

class TodoForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	description = TextAreaField('Description',validators=[DataRequired()])
	completed = SelectField('Completed', choices = [("False", "False"), ("True", "True")], validators = [DataRequired()])
	share_with = StringField('Share with user: (use commas to separate usernames)')
	user_id = HiddenField()
	submit = SubmitField("Submit")

class SignupForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField("Sign Up")
class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = StringField('Password', validators=[DataRequired()])
	submit = SubmitField("Login")
