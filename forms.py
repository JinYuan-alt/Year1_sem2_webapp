from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators
from wtforms.fields import EmailField, DateField, IntegerField
class CreateFormatForm(Form):
    first_name = StringField('name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = IntegerField('phone number', [validators.NumberRange(min=0, max=99999999), validators.DataRequired()])
    gender = EmailField('email', [validators.Email(), validators.DataRequired()])
    membership = RadioField('member', choices=[('F', 'Fellow'), ('S', 'Senior'), ('P', 'Professional')], default='F')
    remarks = TextAreaField('Feedback', [validators.DataRequired()])

class CreateStaffForm(Form):
 first_name = StringField('username', default='scott')
 last_name = StringField('password', [validators.Length(min=1, max=150), validators.DataRequired()])
 gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')],
 default='M')
 email = EmailField('email', default='scott@gmail.com')
 date_joined = DateField('Date Joined', format='%Y-%m-%d', default=None)
 address = IntegerField('Staff ID', [validators.DataRequired()])
 membership = RadioField('Membership',[validators.Optional()],choices=[('S', 'Staff'), ('f', 'fellow'), ('P', 'Professional')], default='',)
 remarks = TextAreaField('Remarks', [validators.Optional()])

