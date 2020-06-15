from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    registration_username = SelectField('Teamnaam',
    choices = sorted([('', 'Selecteer uw teamnaam'), ('GSV Niedermeier', 'GSV Niedermeier'), ('Micronesia Maniacs', 'Micronesia Maniacs'),
    ('Adrianus Albertus \'t Vijfje', 'Adrianus Albertus \'t Vijfje'), ('FC SJHEV', 'FC SJHEV'),
    ('FC Groen Goud', 'FC Groen Goud'), ('Los Banditos', 'Los Banditos'),
    ('v.v. Twenthe 7', 'v.v. Twenthe 7'), ('FC Kuitkramp', 'FC Kuitkramp'),
    ('Boca Seniors', 'Boca Seniors'), ('Newton Heath', 'Newton Heath')]), validators = [DataRequired()])
    registration_email = StringField('Email', validators=[DataRequired(), Email()])
    registration_password = PasswordField('Password', validators=[DataRequired()])
    registration_confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('registration_password')])
    submit = SubmitField('Opslaan')

class TeamForm(FlaskForm):
    team_username = SelectField('Teamnaam',
    choices = sorted([('', 'Selecteer uw teamnaam'), ('GSV Niedermeier', 'GSV Niedermeier'), ('Micronesia Maniacs', 'Micronesia Maniacs'),
    ('Adrianus Albertus \'t Vijfje', 'Adrianus Albertus \'t Vijfje'), ('FC SJHEV', 'FC SJHEV'),
    ('FC Groen Goud', 'FC Groen Goud'), ('Los Banditos', 'Los Banditos'),
    ('v.v. Twenthe 7', 'v.v. Twenthe 7'), ('FC Kuitkramp', 'FC Kuitkramp'),
    ('Boca Seniors', 'Boca Seniors'), ('Newton Heath', 'Newton Heath')]), validators = [DataRequired()])
    team_password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Team bekijken')
