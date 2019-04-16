import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FILE_FOLDER = 'files'

    # 以下 3 条内容需要向 evercad 申请
    EVERCAD_USERNAME = os.environ.get('EVERCAD_USERNAME') or 'username'
    EVERCAD_PWD = os.environ.get('EVERCAD_PWD') or 'pwd'
    CLIENTID = os.environ.get('CLIENTID') or 'your client id'

    EVERCAD_UPLOAD_URL = 'https://test.everxyz.com/stp/upload'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
