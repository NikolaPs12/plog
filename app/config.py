import os

from dotenv import load_dotenv

load_dotenv()

class Config(object):
    APPNAME = 'app'
    ROOT = os.path.abspath(APPNAME)
    UPLOAD_PATH = 'static/profile_pics'
    SERVER_PATH = os.path.join(ROOT, UPLOAD_PATH.lstrip('/'))

    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY") or "supersecret"
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300  


    # Используем переменную окружения для подключения к БД с явным указанием кодировки
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "postgresql://plog:password@localhost:5432/dbplog"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nikola'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {
            'client_encoding': 'utf8'
        }
    }
    MAIL_SERVER = os.getenv("MAIL_SERVER")          # например smtp.gmail.com
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))    # обычно 587 для TLS
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")      # твой email
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")      # пароль или app password
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", MAIL_USERNAME)
