from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class RoleForm(FlaskForm):
    role = SelectField(
        'Role',
        choices=[('admin', 'Admin'), ('author', 'Author'), ('user', 'User')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Change')
