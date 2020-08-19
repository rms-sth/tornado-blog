from wtforms import Form, TextAreaField, StringField, validators


class BlogForm(Form):
    title = StringField("Title", [validators.Length(min=4, max=25)])
    text = TextAreaField("Blog Description")

