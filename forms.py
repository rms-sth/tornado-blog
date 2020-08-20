from wtforms import Form, TextAreaField, StringField, validators
from wtforms.widgets.core import PasswordInput


class BlogForm(Form):
    title = StringField("Title", [validators.Length(min=4, max=25)])
    text = TextAreaField("Blog Description")


class LoginForm(Form):
    username = StringField("Username")
    password = StringField('Password', widget=PasswordInput(hide_value=False))
