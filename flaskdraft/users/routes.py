from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from flaskdraft import db, bcrypt
from flaskdraft.models import registration, bid
from flaskdraft.users.forms import RegistrationForm, TeamForm
from datetime import datetime
from sqlalchemy import func
import pytz

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form_registration = RegistrationForm()
    if request.method == 'POST' and form_registration.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form_registration.registration_password.data).decode('utf-8')
        user_query = registration.query.filter_by(user = form_registration.registration_username.data).first()
        if user_query != None:
            if bcrypt.check_password_hash(user_query.user_password, form_registration.registration_password.data):
                user_query.user_email = form_registration.registration_email.data
                user_query.user_password = hashed_password
                db.session.commit()
                flash('Uw gegevens zijn bijgewerkt!', 'bottom')
            else:
                flash('Verkeerd huidig wachtwoord!', 'bottom')
        else:
                user_registration = registration(user = form_registration.registration_username.data, user_email = form_registration.registration_email.data, user_password = hashed_password)
                db.session.add(user_registration)
                db.session.commit()
                flash('Uw gegevens zijn ingevoegd!', 'bottom')

    return render_template('registration.html', form_registration = form_registration)

@users.route('/team_login', methods=['GET', 'POST'])
def team_login():
    form_team = TeamForm()
    if request.method == 'POST' and form_team.validate_on_submit():
        password_query = registration.query.filter_by(user=form_team.team_username.data).first()
        if bcrypt.check_password_hash(password_query.user_password, form_team.team_password.data):
            session['team'] = form_team.team_username.data
            return redirect(url_for('users.team'))
        else:
            flash('Verkeerd wachtwoord!', 'bottom')
    return render_template('team_check.html', form_team = form_team)

@users.route('/team', methods=['GET', 'POST'])
def team():
    subq = bid.query.distinct(bid.player_id).order_by(bid.player_id, bid.date_bid.desc()).subquery()
    rows = bid.query.select_entity_from(subq).filter_by(username=session.get('team')).order_by(bid.date_bid.desc()).all()
    confirmed_list = []
    total_spent = 0
    total_pending_spent = 0
    team_budget = 400
    for row in rows:
        elapsed_time = (datetime.utcnow() - row.date_bid).total_seconds()
        elapsed_time_hours = float(elapsed_time // 3600)
        if  elapsed_time_hours >= 12:
            confirmed_list.append("True")
            total_spent = total_spent + row.user_bid
        else:
            confirmed_list.append("False")
            total_pending_spent = total_pending_spent + row.user_bid
        row.date_bid = row.date_bid.replace(tzinfo=pytz.utc)
        tz = pytz.timezone('Europe/Amsterdam')
        row.date_bid = row.date_bid.astimezone(tz)
    current_budget = team_budget - total_spent
    current_pending_budget = current_budget - total_pending_spent
    return render_template('team.html', rows = rows, header = session.get('team'), confirmed_list = confirmed_list, total_spent = total_spent,
                            total_pending_spent = total_pending_spent, current_pending_budget = current_pending_budget, current_budget = current_budget)
