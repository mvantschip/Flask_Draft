from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    registration_username = SelectField('Teamnaam',
    choices = sorted([('', 'Selecteer uw teamnaam'), ('GSV Niedermeier', 'GSV Niedermeier'), ('Micronesia Maniacs', 'Micronesia Maniacs'),
    ('Adrianus Albertus \'t Vijfje', 'Adrianus Albertus \'t Vijfje'), ('FC SJHEV', 'FC SJHEV'),
    ('FC Groen Goud', 'FC Groen Goud'), ('Los Banditos', 'Los Banditos'),
    ('v.v. Twenthe 7', 'v.v. Twenthe 7'), ('FC Kuitkramp', 'FC Kuitkramp'),
    ('Mocro\'s Mannen', 'Mocro\'s Mannen'), ('Newton Heath', 'Newton Heath')]), validators = [DataRequired()])
    registration_email = StringField('E-mailadres', validators=[DataRequired(), Email()])
    registration_password = PasswordField('Wachtwoord', validators=[DataRequired()])
    registration_confirm_password = PasswordField('Bevestig wachtwoord', validators=[DataRequired(), EqualTo('registration_password')])
    registration_current_password = PasswordField('Huidig wachtwoord')
    submit = SubmitField('Opslaan')

class TeamForm(FlaskForm):
    team_username = SelectField('Teamnaam',
    choices = sorted([('', 'Selecteer uw teamnaam'), ('GSV Niedermeier', 'GSV Niedermeier'), ('Micronesia Maniacs', 'Micronesia Maniacs'),
    ('Adrianus Albertus \'t Vijfje', 'Adrianus Albertus \'t Vijfje'), ('FC SJHEV', 'FC SJHEV'),
    ('FC Groen Goud', 'FC Groen Goud'), ('Los Banditos', 'Los Banditos'),
    ('v.v. Twenthe 7', 'v.v. Twenthe 7'), ('FC Kuitkramp', 'FC Kuitkramp'),
    ('Boca Seniors', 'Boca Seniors'), ('Newton Heath', 'Newton Heath')]), validators = [DataRequired()])
    team_password = PasswordField('Wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Team bekijken')
