from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    from .routes.auth import auth_bp
    from .routes.player import player_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(player_bp, url_prefix='/player')
    
    with app.app_context():
        db.create_all()
    
    return app