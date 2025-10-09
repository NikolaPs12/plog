import os

from dotenv import load_dotenv

load_dotenv()

class Config(object):
    APPNAME = 'app'
    ROOT = os.path.abspath(APPNAME)
    UPLOAD_PATH = 'static/profile_pics'
    SERVER_PATH = os.path.join(ROOT, UPLOAD_PATH.lstrip('/'))

    # Используем переменную окружения для подключения к БД с явным указанием кодировки
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "postgresql://plog:password@localhost:5432/dbplog"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nikola'
    SQLALCHEMY_TRACK_MODIFICATIONS = True # Изменено на False для производительности
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {
            'client_encoding': 'utf8'
        }
    }