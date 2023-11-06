from wtforms import Form, StringField, TextAreaField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired


class PostForm(Form):
    image = FileField('Select Image', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    title = StringField('Title')
    body = TextAreaField('Body')