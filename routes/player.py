from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from .. import db
from sqlalchemy.sql import text

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
        query = text("""
            SELECT p.player_id, p.first_name, p.last_name, t.team_name, p.position, p.jersey_number
            FROM player p
            JOIN team t ON p.team_id = t.team_id
            WHERE p.first_name LIKE :term OR p.last_name LIKE :term
        """)
        players = db.session.execute(query, {'term': f'%{search_term}%'}).fetchall()
    
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
        
        try:
            query = text("""
                INSERT INTO player (first_name, last_name, team_id, nationality, birth_date, position, jersey_number)
                VALUES (:first_name, :last_name, :team_id, :nationality, :birth_date, :position, :jersey_number)
            """)
            db.session.execute(query, {
                'first_name': first_name,
                'last_name': last_name,
                'team_id': team_id,
                'nationality': nationality,
                'birth_date': birth_date,
                'position': position,
                'jersey_number': jersey_number
            })
            db.session.commit()
            flash('Player added successfully!')
            return redirect(url_for('player.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding player: {str(e)}')
    
    teams = db.session.execute(text("SELECT team_id, team_name FROM team")).fetchall()
    return render_template('add_player.html', teams=teams)