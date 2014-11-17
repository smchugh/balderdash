# Import input types such as TextField
from wtforms import StringField, PasswordField, IntegerField, BooleanField

# Import input validators
from wtforms.validators import InputRequired, EqualTo, Length, NumberRange, Optional, Email, URL

# Import Base inputs class
from application.inputs.Base import Base

# Import the Player model
from application.models.Player import Player


# Define the player list inputs
class ListInputs(Base):
    offset = IntegerField(
        'Offset',
        [Optional(), NumberRange(min=0)]
    )

    limit = IntegerField(
        'Limit',
        [Optional(), NumberRange(min=0)]
    )


# Define the player creation inputs
class CreateInputs(Base):
    username = StringField(
        'Username',
        [
            InputRequired(message='Must provide a username'),
            Length(
                max=Player.USERNAME_MAX_LENGTH,
                message='Username can not be more than {} characters'.format(Player.USERNAME_MAX_LENGTH)
            )
        ]
    )

    password = PasswordField(
        'Password',
        [
            InputRequired(message='Must provide a password'),
            Length(
                max=Player.PASSWORD_MAX_LENGTH,
                message='Password can not be more than {} characters'.format(Player.PASSWORD_MAX_LENGTH)
            ),
            EqualTo('confirm', message='Passwords must match'),
        ]
    )

    confirm = PasswordField(
        'Confirm Password',
        [InputRequired(message='Must confirm your password')]
    )

    email = StringField(
        'Email',
        [InputRequired(message='Must provide and email address'), Email()]
    )

    avatar_url = StringField(
        'Avatar URL',
        [Optional(), URL()]
    )


# Define the player update inputs
class UpdateInputs(Base):
    username = StringField(
        'Username',
        [
            Optional(),
            Length(
                max=Player.USERNAME_MAX_LENGTH,
                message='Username can not be more than {} characters'.format(Player.USERNAME_MAX_LENGTH)
            )
        ]
    )

    password = PasswordField(
        'Password',
        [
            Optional(),
            Length(
                max=Player.PASSWORD_MAX_LENGTH,
                message='Password can not be more than {} characters'.format(Player.PASSWORD_MAX_LENGTH)
            )
        ]
    )

    email = StringField(
        'Email',
        [Optional(), Email()]
    )

    avatar_url = StringField(
        'Avatar URL',
        [Optional(), URL()]
    )

    is_active = BooleanField(
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
