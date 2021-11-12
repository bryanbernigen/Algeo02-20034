
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField,IntegerField, Form
from wtforms import validators
from wtforms.validators import InputRequired


class PostForm(FlaskForm):
    picture = FileField('Insert picture', validators=[InputRequired(),FileAllowed(['jpg', 'jpeg', 'png'], 'images only')])
    scale = IntegerField('Insert Scale 0 ... 100', [validators.NumberRange(min=0, max=100)])
    submit=SubmitField('submit')