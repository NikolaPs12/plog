from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
from flask_mail import Mail
from flask_compress import Compress
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})
compress = Compress()
mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()