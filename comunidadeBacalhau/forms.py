from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, length, email, EqualTo, ValidationError
from comunidadeBacalhau.models import User


class FormCriarConta(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), length(4, 20)])
    email = StringField("E-mail", validators=[DataRequired(), email()])
    password = PasswordField("Password", validators=[DataRequired(), length(6, 20)])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password")])
    button_submit_criarconta = SubmitField("Create an account")

    # verificando se ja existe um usuario com o mesmo email
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already registered")


class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), email()])
    password = PasswordField("Password", validators=[DataRequired(), length(6, 20)])
    remember_password = BooleanField("Remember password")
    button_submit_login = SubmitField("Login")


class FormResetPassword(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), length(6, 20)])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password")])
    button_submit_reset = SubmitField("Reset Password")


class FormEditPost(FlaskForm):
    title = StringField("Titulo", validators=[DataRequired()])
    content = TextAreaField("Reescreva seu post", validators=[DataRequired()])
    button_submit_edit_post = SubmitField("Editar Post")


class FormCreatePost(FlaskForm):
    title = StringField("Título", validators=[DataRequired(), length(4, 100)])
    content = TextAreaField("Escreva seu post", validators=[DataRequired()])
    button_submit_create_post = SubmitField("Criar Post")


class FormSearch(FlaskForm):
    search = StringField("Search", validators=[DataRequired()])
    button_submit_search = SubmitField("Search")
    
    

class FormEditCourse(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    button_submit_edit = SubmitField("Editar curso")


class FormCreateCourse(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    button_submit = SubmitField("Criar curso")


class FormEditprofile(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), length(4, 20)])
    email = StringField("E-mail", validators=[DataRequired(), email()])
    profile_picture = FileField("Alterar foto", validators=[FileAllowed(["jpg", "png", "jpeg"])])
    button_submit_edit_profile = SubmitField("Confirmar")

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email already registered")


class FormContact(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), email()])
    subject = StringField("Subject", validators=[DataRequired()])
    message = StringField("Message", validators=[DataRequired()])
    button_submit = SubmitField("Send")
    