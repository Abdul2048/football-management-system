from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user
from .config import Config
from .models.user import User
import mysql.connector
import logging
import sys

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

login_manager = LoginManager()

def create_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database="football"
        )
        logging.info("Successfully connected to MySQL database 'football'")
        return conn
    except mysql.connector.Error as e:
        logging.error(f"Failed to connect to MySQL database: {str(e)}")
        raise Exception(f"Database connection failed: {str(e)}")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Verify database connection at startup
    try:
        conn = create_db_connection()
        conn.close()
        print("Database connection verified successfully", file=sys.stderr)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        logging.critical(f"Application startup failed due to database error: {str(e)}")
        raise
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        conn = create_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        if user_data:
            return User(user_data['id'], user_data['username'], user_data['password_hash'])
        return None
    
    from .routes.auth import auth_bp
    from .routes.player import player_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(player_bp, url_prefix='/player')
    
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('player.dashboard'))
        return redirect(url_for('auth.login'))
    
    return app