from wtforms import Form, StringField, TextAreaField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired


class PostForm(Form):
   # filepath = FileField('Select Image', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'png/jpg only!')])
    filepath = FileField('Select Image', validators=[FileAllowed(['jpg', 'png'], 'png/jpg only!')])
    title = StringField('Title')
    body = TextAreaField('Body')