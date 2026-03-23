from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms.fields import (
    StringField, EmailField, PasswordField, SubmitField, 
    BooleanField, TextAreaField, SelectMultipleField)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from WWE.models import User
from WWE.extensions import db



class RegisterForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(max=20, min=4)])
    email = EmailField(label='Email Address', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField(label='Register')

    def validate_username(self, username):
        user = db.session.scalar(db.select(User).where(User.username == username.data))
        if user:
            raise ValidationError('That username is taken. Please choose different one!')

    def validate_email(self, email):
        user = db.session.scalar(db.select(User).where(User.email == email.data))
        if user:
            raise ValidationError('That email is taken. Please choose different one!')


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember = BooleanField(label='Remember Me')

    submit = SubmitField(label='Login')


class UpdateAccountForm(FlaskForm):
    username = StringField(
        label='Username',
        validators=[DataRequired(), Length(min=4, max=20)],
        render_kw={'readonly': 'readonly'}
    )
    email = EmailField(
        label='Email',
        validators=[DataRequired(), Email()],
        render_kw={'readonly': 'readonly'}
    )
    fullname = StringField(label='Fullname', render_kw={'placeholder': 'Enter Fullname'})
    avatar = FileField(label='Update Profile Avatar', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

    submit = SubmitField(label='Update Account')

class WWEForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    height = StringField('Height', validators=[DataRequired()])
    weight = StringField('Weight', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    
    types = SelectMultipleField('Types', coerce=int)
    submit = SubmitField('Submit')