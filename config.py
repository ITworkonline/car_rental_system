import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    #secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A-VERY-LONG-SECRET-KEY'

    #database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '1130'
    MYSQL_DB = 'mysql'
    MYSQL_CURSORCLASS = 'DictCursor'