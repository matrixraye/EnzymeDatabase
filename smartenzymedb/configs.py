class BaseConfig:
    """ 配置基类 """

    SECRET_KEY = 'makesure to set a very secret key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """ 开发环境配置 """

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///enzymedb.db'


class ProductionConfig(BaseConfig):
    """ 生产环境配置 """

    pass


class TestingConfig(BaseConfig):
    """ 测试环境配置 """

    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}