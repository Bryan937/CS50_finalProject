from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from website.models import User, Grade, Subject, Post

def grade_query():
    return Grade.query

def subject_query():
    return Subject.query

# Fields that the user will have to fill in the signup form
class SignupForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    grade = QuerySelectField(query_factory=grade_query, validators=[DataRequired()],
                            allow_blank=True, blank_text='Choose a Grade..', get_label='name')
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=2, max=50)])
    confirm = PasswordField('Repeat Password',
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # Ensure username is unique
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    
    # Ensure email is unique
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken. Please choose a different one.')


# Fields that the user will have to fill in the login form
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(),])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


# Fields that the user will have to fill in the Update Profile form
class UpdateProfileForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    grade = QuerySelectField(query_factory=grade_query,
                            allow_blank=True, blank_text='Choose a Grade..',  get_label='name')
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only (jpg, jpeg, png)')])
    submit = SubmitField('Update')

    # Ensure username is unique
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
    
    # Ensure email is unique
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is taken. Please choose a different one.')


# Fields that the user will have to fill in the Post form
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subject = QuerySelectField(query_factory=subject_query, allow_blank=True,
                              blank_text='Choose a Subject..', get_label='name', validators=[DataRequired()])
    grade = QuerySelectField(query_factory=grade_query, allow_blank=True,
                            blank_text='Choose a Grade..', get_label='name', validators=[DataRequired()])
    question = TextAreaField('Question',
                            validators=[DataRequired()])
    answer = TextAreaField('Answer',
                          validators=[DataRequired()])
    submit = SubmitField('Post')


# Fields that the user will have to fill in the Post form
class SearchForm(FlaskForm):
    subject = QuerySelectField(query_factory=subject_query, allow_blank=True,
                              blank_text='Choose a Subject..', get_label='name', validators=[DataRequired()])
    grade = QuerySelectField(query_factory=grade_query, allow_blank=True,
                            blank_text='Choose a Grade..', get_label='name', validators=[DataRequired()])
    submit = SubmitField('Filter')