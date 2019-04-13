import os
basedir=os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY')or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    FLASKY_LOGIC_PER_PAGE = 20
    @staticmethod
    def init_app(app):
        pass
class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI ='mysql+pymysql://root:diaoxuyang@localhost:3306/gas_info'
config={
    'development':DevelopmentConfig,
    'default':DevelopmentConfig
}