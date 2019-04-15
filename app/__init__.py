import os

from flask import Flask, g, url_for
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config


bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please login to view this page'

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.groups import bp as groups_bp
    app.register_blueprint(groups_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, prefix='/auth')

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp)

    return app


from app import models
