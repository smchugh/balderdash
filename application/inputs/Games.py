# Import input types such as TextField
from wtforms import StringField, IntegerField, BooleanField

# Import input validators
from wtforms.validators import InputRequired, Length, NumberRange, Optional

# Import Base inputs class
from application.inputs.Base import Base

# Import the Game class
from application.models.Game import Game


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
                max=Game.NAME_MAX_LENGTH,
                message='Game name can not be more than {} characters'.format(Game.NAME_MAX_LENGTH)
            )
        ]
    )

    description = StringField(
        'Description',
        [
            InputRequired(message='Must provide a description'),
            Length(
                max=Game.DESCRIPTION_MAX_LENGTH,
                message='Game description can not be more than {} characters'.format(
                    Game.DESCRIPTION_MAX_LENGTH
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
                max=Game.NAME_MAX_LENGTH,
                message='Game name can not be more than {} characters'.format(Game.NAME_MAX_LENGTH)
            )
        ]
    )

    description = StringField(
        'Description',
        [
            Optional(),
            Length(
                max=Game.DESCRIPTION_MAX_LENGTH,
                message='Game description can not be more than {} characters'.format(
                    Game.DESCRIPTION_MAX_LENGTH
                )
            )
        ]
    )

    is_active = BooleanField(
        'Active',
        [Optional()]
    )
