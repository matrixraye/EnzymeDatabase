import os
from urllib.parse import quote_plus

class BaseConfig:
    """ 配置基类 """

    SECRET_KEY = 'makesure to set a very secret key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def get_db_credentials():
        credentials = {}
        with open(os.path.join(os.path.dirname(__file__), "password.txt")) as f:
            for line in f:
                if line.strip() and '=' in line:
                    key, value = line.strip().split('=', 1)
                    credentials[key] = value
        return credentials


class DevelopmentConfig(BaseConfig):
    """ 开发环境配置 """

    DEBUG = True
    creds = BaseConfig.get_db_credentials()
    # URL encode the password
    encoded_password = quote_plus(creds["password"])
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{creds["username"]}:{encoded_password}@localhost:5432/test_db'


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