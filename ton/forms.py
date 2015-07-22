from wtforms import Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import ValidationError, Required, Email, Length

from .models import User


# unique validator
class Unique(object):
    def __init__(self, model, field, message):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        if self.model.query.filter(self.field == field.data).first():
            raise ValidationError(self.message)



class RegisterForm(Form):
    unique_email = Unique(User, User.email, message='this email has already been used')
    email = TextField(validators=[Required(), Email(), unique_email])
    password = PasswordField(validators=[Required(), Length(min=8, max=30, message='password must be at least 8 characters')])


class LoginForm(Form):
    email = TextField(validators=[Required(), Email()])
    password = PasswordField(validators=[Required()])
