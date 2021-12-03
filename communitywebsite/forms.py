from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from communitywebsite.models import Customer
from flask_login import current_user


class FormCreateAccount(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    email = StringField('e-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    password_validation = PasswordField('Password Confirmation', validators=[DataRequired(), EqualTo('password')])
    create_button_submit = SubmitField('Account Creator')

    def validate_email(self, email):
        user = Customer.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('e-Mail already registered. use another e-Mail or Login on the left side')


class FormLogin(FlaskForm):
    email = StringField('e-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    data_remember = BooleanField('Remind my data')
    login_submit_button = SubmitField('Login')


class FormEditProfile(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    email = StringField('e-Mail', validators=[DataRequired(), Email()])
    user_picture = FileField('Select your best photo', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    class_excel = BooleanField('Excel')
    class_vba = BooleanField('VBA')
    class_powerbi = BooleanField('PowerBI')
    class_python = BooleanField('Python')
    class_sql = BooleanField('SQL')
    edit_profile_button = SubmitField('Save Edit')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = Customer.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('e-Mail already registered. use another e-Mail')


class FormCreatePost(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired(), Length(2, 140)])
    body = TextAreaField('Write your Post', validators=[DataRequired()])
    create_post_button = SubmitField('Save Post')
