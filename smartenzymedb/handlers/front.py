from flask import Blueprint, render_template
from smartenzymedb.forms import LoginForm, RegisterForm
from flask import redirect, url_for
from flask_login import login_user
from smartenzymedb.models import User

# 省略了 url_prefix，那么默认就是 '/'
front = Blueprint('front', __name__)

@front.route('/')
def index():
    return render_template('index.html')

@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)


@front.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()                  # 新增
        return redirect(url_for('.login'))  # 新增
    return render_template('register.html', form=form)