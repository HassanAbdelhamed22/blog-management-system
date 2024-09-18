from flask_wtf import FlaskForm
from wtforms import SubmitField

class DislikeForm(FlaskForm):
    submit = SubmitField('Dislike')