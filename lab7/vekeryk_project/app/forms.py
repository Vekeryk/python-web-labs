from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, BooleanField, ValidationError
from wtforms.validators import Email, DataRequired, EqualTo, Length, Regexp
from app.models import User


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), 
                        Length(min=4, max=10, message='Name length must be between %(min)d and %(max)d')])
    email = StringField("Email", validators=[DataRequired(), Email(message='Email is invalid')])
    phone = StringField("Phone", validators=[Regexp(regex='^\+380[0-9]{9}$', message='Phone is invalid')])
    subject = SelectField("Subject", 
                          choices=[('1', 'Bug report'), ('2', 'Cooperation'), ('3', 'Suggestions')],
                          render_kw={"class": "form-select"})
    message = TextAreaField("Message", validators=[Length(max=500, message='Message is too long')])
    submit = SubmitField("Send")


class RegistrationForm(FlaskForm):
    username = StringField("Username", 
                           validators=[DataRequired(), 
                           Length(min=4, max=25, 
                           message='Username length must be between 4 and 25'),
                           Regexp(regex='^[A-Za-z][A-Za-z0-9_.]*$',
                           message='Username can contains lettes, numbers, dots and underscores')])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[Length(min=6,
                             message='Password must be longer then 6')])
    confirm_password = PasswordField('Confirm password',
                             validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign up")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(message='Email is invalid')])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me", render_kw={"class": "form-check-input"})
    submit = SubmitField("Login")
