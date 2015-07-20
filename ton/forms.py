from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import Required, Email

from wtforms.validators import ValidationError

from .models import User


# unique validator
class Unique(object):
    def __init__(self, model, field, message=u'This element alredy exists.'):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)



class EmailPasswordForm(Form):
    email = TextField('Email', validators=[Required(), Email(),
                                           Unique(
                                               User,
                                               User.email,
                                               message='Sorry, this email has already been used.'
                                           )])
    password = PasswordField('Password', validators=[Required()])


class LoginForm(Form):
    email = TextField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])

