import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

# extensions:
db = SQLAlchemy()
ma = Marshmallow()

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from main.routes import main
    from errors.handlers import errors
    from users.routes import users
    from posts.routes import posts
    from api.routes import api

    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(api)
    return app