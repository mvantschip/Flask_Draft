from flask import Blueprint, render_template, request, flash
from flaskdraft import db, bcrypt
from flaskdraft.models import registration
from flaskdraft.users.forms import RegistrationForm


users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form_registration = RegistrationForm()
    if request.method == 'POST' and form_registration.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form_registration.registration_password.data).decode('utf-8')
        user_query = registration.query.filter_by(user = form_registration.registration_username.data).first()
        if user_query != None:
            user_query.user_email = form_registration.registration_email.data
            user_query.user_password = hashed_password
            db.session.commit()
            flash('Uw gegevens zijn bijgewerkt!', 'bottom')
        else:
            user_registration = registration(user = form_registration.registration_username.data, user_email = form_registration.registration_email.data, user_password = hashed_password)
            db.session.add(user_registration)
            db.session.commit()
            flash('Uw gegevens zijn ingevoegd!', 'bottom')
    return render_template('registration.html', form_registration = form_registration)
