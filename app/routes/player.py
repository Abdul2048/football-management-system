from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from .. import create_db_connection

player_bp = Blueprint('player', __name__)

@player_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@player_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    players = []
    if request.method == 'POST':
        search_term = request.form.get('search_term')
        conn = create_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT p.player_id, p.first_name, p.last_name, t.team_name, p.position, p.jersey_number
            FROM player p
            JOIN team t ON p.team_id = t.team_id
            WHERE p.first_name LIKE %s OR p.last_name LIKE %s
        """
        cursor.execute(query, (f'%{search_term}%', f'%{search_term}%'))
        players = cursor.fetchall()
        cursor.close()
        conn.close()
    
    return render_template('player_search.html', players=players)

@player_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_player():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        team_id = request.form.get('team_id')
        nationality = request.form.get('nationality')
        birth_date = request.form.get('birth_date')
        position = request.form.get('position')
        jersey_number = request.form.get('jersey_number')
        
        conn = create_db_connection()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO player (first_name, last_name, team_id, nationality, birth_date, position, jersey_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (first_name, last_name, team_id, nationality, birth_date, position, jersey_number))
            conn.commit()
            flash('Player added successfully!')
            cursor.close()
            conn.close()
            return redirect(url_for('player.dashboard'))
        except Exception as e:
            conn.rollback()
            flash(f'Error adding player: {str(e)}')
            cursor.close()
            conn.close()
    
    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT team_id, team_name FROM team")
    teams = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('add_player.html', teams=teams)