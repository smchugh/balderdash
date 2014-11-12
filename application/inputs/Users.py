# Import Form for input validation
from flask.ext.wtf import Form

# Import Form elements such as TextField
from wtforms import StringField, PasswordField, IntegerField, BooleanField

# Import Form validators
from wtforms.validators import InputRequired, EqualTo, Length, NumberRange, Optional

from settings import settings


class Base(Form):
    def obfuscated(self):
        inputs = {}
        for name in dir(self):
            if not name.startswith('__'):
                attribute = getattr(self, name)
                if hasattr(attribute, 'data'):
                    inputs[name] = attribute.data

        if inputs.get('password') is not None:
            inputs['password'] = None

        return inputs


# Define the user list inputs
class ListInputs(Base):
    offset = IntegerField(
        'Offset',
        [Optional(), NumberRange(min=0)]
    )

    limit = IntegerField(
        'Limit',
        [Optional(), NumberRange(min=0)]
    )


# Define the user creation inputs
class CreateInputs(Base):
    username = StringField(
        'Username',
        [
            InputRequired(message='Must provide a username'),
            Length(
                max=settings.USERNAME_MAX_LENGTH,
                message='Username can not be more than {} characters'.format(settings.USERNAME_MAX_LENGTH)
            )
        ]
    )

    password = PasswordField(
        'Password',
        [
            InputRequired(message='Must provide a password'),
            Length(
                max=settings.PASSWORD_MAX_LENGTH,
                message='Password can not be more than {} characters'.format(settings.PASSWORD_MAX_LENGTH)
            ),
            EqualTo('confirm', message='Passwords must match'),
        ]
    )

    confirm = PasswordField(
        'Confirm Password',
        [InputRequired(message='Must confirm your password')]
    )


# Define the user creation inputs
class UpdateInputs(Base):
    username = StringField(
        'Username',
        [
            Optional(),
            Length(
                max=settings.USERNAME_MAX_LENGTH,
                message='Username can not be more than {} characters'.format(settings.USERNAME_MAX_LENGTH)
            )
        ]
    )

    password = PasswordField(
        'Password',
        [
            Optional(),
            Length(
                max=settings.PASSWORD_MAX_LENGTH,
                message='Password can not be more than {} characters'.format(settings.PASSWORD_MAX_LENGTH)
            )
        ]
    )

    active = BooleanField(
        'Active',
        [Optional()]
    )


# Define the sign in inputs
class SignInInputs(Base):
    username = StringField(
        'Username',
        [InputRequired(message='Must provide a username')]
    )

    password = PasswordField(
        'Password',
        [InputRequired(message='Must provide a password')]
    )
