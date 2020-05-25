from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class PlayerConfirm(FlaskForm):
    player = SelectField('Speler kiezen', validators = [DataRequired()])
    submit = SubmitField('Speler kiezen')
