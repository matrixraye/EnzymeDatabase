from flask import Blueprint, render_template, redirect, url_for, request
from smartenzymedb.models import db, User, BasicInformation
from smartenzymedb.forms import LoginForm, RegisterForm, SearchForm, AdvancedSearchForm
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

@front.route('/search', methods=['GET', 'POST'])
def search():
    quick_form = SearchForm()
    advanced_form = AdvancedSearchForm()
    results = None
    if request.method == 'POST':
        if 'quick_search' in request.form and quick_form.validate():
            search_query = quick_form.query.data
            # 假设搜索在 BasicInformation 表的 ProteinName、ECNumber、Organism 等字段中进行
            results = BasicInformation.query.filter(
                db.or_(
                    BasicInformation.ProteinName.ilike(f"%{search_query}%"),
                    BasicInformation.ECNumber.ilike(f"%{search_query}%"),
                    BasicInformation.Organism.ilike(f"%{search_query}%"),
                    BasicInformation.UniprotID.ilike(f"%{search_query}%")
                )
            ).all()
        # 处理GET请求，执行高级搜索
        elif 'advanced_search' in request.form and advanced_form.validate():
            filters = []
            if advanced_form.ProteinName.data:
                filters.append(BasicInformation.ProteinName.ilike(f"%{advanced_form.ProteinName.data}%"))
            if advanced_form.ECNumber.data:
                filters.append(BasicInformation.ECNumber.ilike(f"%{advanced_form.ECNumber.data}%"))
            if advanced_form.Organism.data:
                filters.append(BasicInformation.Organism.ilike(f"%{advanced_form.Organism.data}%"))
            if advanced_form.UniprotID.data:
                filters.append(BasicInformation.UniprotID.ilike(f"%{advanced_form.UniprotID.data}%"))

            results = BasicInformation.query.filter(*filters).all()
    return render_template('search.html', quick_form=quick_form, advanced_form=advanced_form, results=results)

@front.route('/browse')
@front.route('/browse/page/<int:page>')
def browse(page=1):
    per_page = 20  # 每页显示的记录数
    pagination = BasicInformation.query.paginate(page=page, per_page=per_page, error_out=False)
    records = pagination.items
    return render_template('browse.html', records=records, pagination=pagination)

@front.route('/help')
def help():
    return render_template('help.html')