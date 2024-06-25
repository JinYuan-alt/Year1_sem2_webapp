from wtforms import Form, StringField, validators

class CreateUserFormSignup(Form):
    username = StringField('Username')
    password = StringField('Password')