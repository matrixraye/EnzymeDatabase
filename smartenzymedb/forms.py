from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import Length, Email, EqualTo, DataRequired, Optional
from .models import db, User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 24)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 24)])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def __init__(self):
        super().__init__()
        print(list(self._fields))


    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在。')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册。')

    def create_user(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 24)])
    remember_me = BooleanField('Remember ME')
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未注册。')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('用户密码错误。')

class SearchForm(FlaskForm):
    query = StringField('', validators=[DataRequired()])
    submit = SubmitField('搜索')

class AdvancedSearchForm(FlaskForm):
    ProteinName = StringField('蛋白质名称', validators=[Optional()])
    ECNumber = StringField('EC 号', validators=[Optional()])
    Organism = StringField('生物体', validators=[Optional()])
    UniprotID = StringField('Uniprot ID', validators=[Optional()])
    submit = SubmitField('搜索')