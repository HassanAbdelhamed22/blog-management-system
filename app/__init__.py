from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
mongo = PyMongo()

def create_app():
    # Create Flask Application
    app = Flask(__name__)

    # Load the Configuration
    app.config.from_object(Config)
    
    # CSRF tokens
    csrf = CSRFProtect(app)

    # Load Extensions
    db.init_app(app)
    mongo.init_app(app)
    csrf.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    # Ensure the login manager can load the user by ID
    from app.models.sql.user import User
    @login_manager.user_loader
    def load_user(user_id):
        if app.config['DATABASE_BACKEND'] == 'sql':
            from app.models.sql.user import User
            return User.query.get(int(user_id))
        elif app.config['DATABASE_BACKEND'] == 'mongo':
            from app.models.mongo.user import User
            return User.find_one({"_id": user_id})

    # Register Blueprints
    from app.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    
    from app.routes.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix="/admin")
    
    from app.routes.author import author as author_blueprint
    app.register_blueprint(author_blueprint, url_prefix="/author")
    
    from app.routes.user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix="/user")

    # Import models to ensure they are registered
    from app.models.sql.user import User
    from app.models.sql.role import Role
    from app.models.sql.blog import Blog
    from app.models.sql.like import Like
    from app.models.sql.dislike import Dislike

    return app
