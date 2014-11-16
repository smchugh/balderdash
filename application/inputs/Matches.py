# Import input types such as TextField
from wtforms import IntegerField

# Import input validators
from wtforms.validators import InputRequired, NumberRange, Optional

# Import Base inputs class
from application.inputs.Base import Base


# Define the match list inputs
class ListInputs(Base):
    offset = IntegerField(
        'Offset',
        [Optional(), NumberRange(min=0)]
    )

    limit = IntegerField(
        'Limit',
        [Optional(), NumberRange(min=0)]
    )

    game_id = IntegerField(
        'Game ID',
        [Optional(), NumberRange(min=1)]
    )

    player_id = IntegerField(
        'Player ID',
        [Optional(), NumberRange(min=1)]
    )


# Define the match creation inputs
class CreateInputs(Base):
    game_id = IntegerField(
        'Game ID',
        [
            InputRequired(message='Must provide a game ID'),
            NumberRange(min=1)
        ]
    )

    player_id = IntegerField(
        'Player ID',
        [
            InputRequired(message='Must provide a player ID'),
            NumberRange(min=1)
        ]
    )

    opponent_id = IntegerField(
        'Opponent ID',
        [Optional(), NumberRange(min=1)]
    )


# Define the match update inputs
class UpdateInputs(Base):
    pass  #TODO turn updates
