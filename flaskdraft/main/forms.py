from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PlayerSearch(FlaskForm):
    name = StringField('Spelersnaam', validators = [DataRequired()])
    submit = SubmitField('Speler zoeken')
