from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from ..models.user import User
from .. import create_db_connection

from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = create_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user_data and check_password_hash(user_data['password_hash'], password):
            user = User(user_data['id'], user_data['username'], user_data['password_hash'])
            login_user(user)
            return redirect(url_for('player.dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = create_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash('Username already exists')
            cursor.close()
            conn.close()
        else:
            password_hash = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO user (username, password_hash) VALUES (%s, %s)",
                (username, password_hash)
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash('Registration successful! Please login.')
            return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))