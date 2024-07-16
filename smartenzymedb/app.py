from flask import Flask, render_template
from smartenzymedb.configs import configs
from smartenzymedb.models import db
#from flask_migrate import Migrate
from flask_login import LoginManager
from smartenzymedb.models import User



def create_app(config):
    """ App工厂，可以根据传入的 config 名称，加载不同的配置
    """
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    # SQLAlchemy 的初始化方式改为使用 init_app
    db.init_app(app)
    #Migrate(app, db)
    
    register_extensions(app)
    register_blueprints(app)

    return app

def register_blueprints(app):
    """注册蓝图的函数"""

    from .handlers import front, admin, user
    app.register_blueprint(front)
    app.register_blueprint(admin)
    app.register_blueprint(user)

def register_extensions(app):
    # db.init_app(app)
    #Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    login_manager.login_view = 'front.login'