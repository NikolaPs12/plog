__version__ = "1.0.0"
import os
from flask import Flask
from .routes.main import main
from .routes.reg import reg
from .routes.login import login
from .routes.posts import post
from .extensions import db, login_manager, mail, compress, cache
from .models.user import User
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    compress.init_app(app)
    cache.init_app(app)

    app.config.from_object(config_class)
    app.register_blueprint(main)
    app.register_blueprint(reg)
    app.register_blueprint(login)
    app.register_blueprint(post)
    app.config['COMPRESS_MIN_SIZE'] = 500
    app.config['MAIL_PORT'] = 1025      # порт для тестового SMTP
    app.config['MAIL_USERNAME'] = 'psenickijkola@gmail.com'
    app.config['MAIL_PASSWORD'] = None
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = False
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    avatar_folder = os.path.join(app.root_path, app.config['UPLOAD_PATH'])
    if not os.path.exists(avatar_folder):
        os.makedirs(avatar_folder)
        
    with app.app_context():
        db.create_all()
    return app