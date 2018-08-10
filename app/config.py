import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '830e43d331825e4fb0d9f5fe8ae98bfd'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/site.db'
    MAIL_SERVER = 'smtp.live.com'
    MAIL_PORT=25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development' : DevelopmentConfig
}