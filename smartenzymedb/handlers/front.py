from flask import Blueprint, render_template, redirect, url_for
from smartenzymedb.models import db, User
from smartenzymedb.forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required
from flask import flash

# 省略了 url_prefix，那么默认就是 '/'
front = Blueprint('front', __name__)

@front.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        flash('登录成功。', 'success')
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)


@front.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录。', 'success')                # 新增
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录。', 'info')
    return redirect(url_for('.index'))