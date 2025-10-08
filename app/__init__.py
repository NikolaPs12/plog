import os
from flask import Flask
from .routes.main import main
from .routes.reg import reg
from .routes.login import login
from .routes.posts import post
from .extensions import db, login_manager, mail
from .models.user import User


def create_app():
    app = Flask(__name__)
    if 'DATABASE_URL' in os.environ:
        # Продакшен (Render.com)
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace("postgres://", "postgresql://", 1)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    app.register_blueprint(main)
    app.register_blueprint(reg)
    app.register_blueprint(login)
    app.register_blueprint(post)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SECRET_KEY'] = '1234567890'
    app.config['MAIL_SERVER'] = 'localhost'
    app.config['MAIL_PORT'] = 1025      # порт для тестового SMTP
    app.config['MAIL_USERNAME'] = 'test@example.com'
    app.config['MAIL_PASSWORD'] = None
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = False
    app.config['APPNAME'] = 'app'
    app.config['ROOT'] = os.path.abspath(app.config['APPNAME'])
    app.config['UPLOAD_PATH'] = 'static/profile_pics'
    app.config['SERVER_PATH'] = os.path.join(app.config['ROOT'], app.config['UPLOAD_PATH'])
    
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    
    with app.app_context():
        db.create_all()
    return app