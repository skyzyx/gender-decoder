from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, validators


class JobAdForm(FlaskForm):
    texttotest = TextAreaField(u'', [validators.Length(min=1)])
    language = SelectField("English", choices=[("en", "English")], default=("en", "English"))
