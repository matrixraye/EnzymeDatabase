from flask import Blueprint, render_template
from smartenzymedb.models import User


user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/<username>')
def index(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user/detail.html', user=user)