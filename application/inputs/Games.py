# Import input types such as TextField
from wtforms import StringField, IntegerField, BooleanField

# Import input validators
from wtforms.validators import InputRequired, Length, NumberRange, Optional

# Import Base inputs class
from application.inputs.Base import Base

# Import global app settings
from settings import settings


# Define the game list inputs
class ListInputs(Base):
    offset = IntegerField(
        'Offset',
        [Optional(), NumberRange(min=0)]
    )

    limit = IntegerField(
        'Limit',
        [Optional(), NumberRange(min=0)]
    )


# Define the game creation inputs
class CreateInputs(Base):
    name = StringField(
        'Name',
        [
            InputRequired(message='Must provide a name'),
            Length(
                max=settings.GAME_NAME_MAX_LENGTH,
                message='Game name can not be more than {} characters'.format(settings.GAME_NAME_MAX_LENGTH)
            )
        ]
    )

    description = StringField(
        'Description',
        [
            InputRequired(message='Must provide a description'),
            Length(
                max=settings.GAME_DESCRIPTION_MAX_LENGTH,
                message='Game description can not be more than {} characters'.format(
                    settings.GAME_DESCRIPTION_MAX_LENGTH
                )
            )
        ]
    )

    match_size = IntegerField(
        'Players per Match',
        [Optional(), NumberRange(min=0)]
    )


# Define the game update inputs
class UpdateInputs(Base):
    name = StringField(
        'Name',
        [
            Optional(),
            Length(
                max=settings.GAME_NAME_MAX_LENGTH,
                message='Game name can not be more than {} characters'.format(settings.GAME_NAME_MAX_LENGTH)
            )
        ]
    )

    description = StringField(
        'Description',
        [
            Optional(),
            Length(
                max=settings.GAME_DESCRIPTION_MAX_LENGTH,
                message='Game description can not be more than {} characters'.format(
                    settings.GAME_DESCRIPTION_MAX_LENGTH
                )
            )
        ]
    )

    is_active = BooleanField(
        'Active',
        [Optional()]
    )
