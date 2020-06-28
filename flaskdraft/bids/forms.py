from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DecimalField, PasswordField
from wtforms.validators import DataRequired, NumberRange

class PlaceBids(FlaskForm):
    bid_player_name = StringField('Naam speler', validators = [DataRequired()])
    bid_player_value = DecimalField('Bod in miljoenen', places = 2, validators = [NumberRange(min=1, max=250), DataRequired()])
    username = SelectField('Teamnaam', choices = sorted([('', 'Selecteer uw teamnaam'), ('GSV Niedermeier', 'GSV Niedermeier'), ('Micronesia Maniacs', 'Micronesia Maniacs'),
    ('Adrianus Albertus \'t Vijfje', 'Adrianus Albertus \'t Vijfje'), ('FC SJHEV', 'FC SJHEV'), ('FC Groen Goud', 'FC Groen Goud'),
    ('Los Banditos', 'Los Banditos'), ('v.v. Twenthe 7', 'v.v. Twenthe 7'), ('FC Kuitkramp', 'FC Kuitkramp'), ('Mocro\'s Mannen', 'Mocro\'s Mannen'),
    ('Newton Heath', 'Newton Heath')]), validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Bieden')
