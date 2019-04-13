import os
basedir=os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY')or 'hard to guess string'
    MAIL_SERVER=os.environ.get('MAIL_SERVER','smtp.163.com')
    MAIL_PORT=int(os.environ.get('MAIL_PORT','25'))
    MAIL_USE_TLS=os.environ.get('MAIL_USE_TLS','true').lower() in \
            ['true','on',1]

    # MAIL_USE_SSL=os.environ.get('MAIL_USE_SSL','true').lower() in \
    #         ['true','on',1]
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX='[Flasky]'
    FLASKY_MAIL_SENDER=os.environ.get('MAIL_USERNAME')
    # FLASKY_ADMIN=os.environ.get('FLASKY_ADMIN')

    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    FLASKY_LOGIC_PER_PAGE = 20
    @staticmethod
    def init_app(app):
        pass
class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI ='mysql+pymysql://root:yangyangyang123@localhost:3306/gas_info'


config={
    'development':DevelopmentConfig,
    'default':DevelopmentConfig
}