from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()    # 注意这里不再传入 app 了


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    ROLE_USER = 0
    ROLE_ADMIN = 30

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        """ Python 风格的 getter """
        return self._password

    @password.setter
    def password(self, orig_password):
        """ Python 风格的 setter, 这样设置 user.password 就会
        自动为 password 生成哈希值存入 _password 字段
        """
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        """ 判断用户输入的密码和存储的 hash 密码是否相等
        """
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def get_id(self):
        return str(self.user_id)
