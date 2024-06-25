from wtforms import Form, StringField, validators

class CreateUserFormLogin(Form):
    username = StringField('Username')
    password = StringField('Password')