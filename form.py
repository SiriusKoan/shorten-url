from flask_wtf import RecaptchaField, Form
from wtforms import TextField, PasswordField, TextAreaField, StringField, validators

class trans(Form):   
    old_url = StringField('old_url', [validators.DataRequired()])
    new_url = StringField('new url', [validators.DataRequired()])
    recaptcha = RecaptchaField()