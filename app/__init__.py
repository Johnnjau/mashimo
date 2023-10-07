from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
DB_NAME = "database.db"

def create_app():
    """Create a new flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .views import views
    from .auth import auth
    

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    
    from .models import User, Products
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    with app.app_context():
        create_database(app)
    
    return app

def create_database(app):
    """Create a new database if it doesn't already exist"""
    if not path.exists('mashimo/' + DB_NAME):
        db.create_all()
        print('Database created successfully')