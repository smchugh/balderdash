# Import input types such as TextField
from wtforms import IntegerField, BooleanField, SelectMultipleField

# Import input validators
from wtforms.validators import InputRequired, NumberRange, Optional

# Import Base inputs class
from application.inputs.Base import Base


# Define the definition filler list inputs
class ListInputs(Base):
    offset = IntegerField(
        'Offset',
        [Optional(), NumberRange(min=0)]
    )

    limit = IntegerField(
        'Limit',
        [Optional(), NumberRange(min=0)]
    )

    word_id = IntegerField(
        'Word ID',
        [Optional(), NumberRange(min=1)]
    )

    definition_template_id = IntegerField(
        'Definition Template ID',
        [Optional(), NumberRange(min=1)]
    )


# Define the definition filler creation inputs
class CreateInputs(Base):
    definition_template_id = IntegerField(
        'Definition Template ID',
        [
            InputRequired(message='Must provide the word ID'),
            NumberRange(min=1)
        ]
    )

    filler = SelectMultipleField(
        'Definition Filler',
        [InputRequired(message='Must provide the definition filler')],
        choices=[]
    )

    is_dictionary = BooleanField(
        'Dictionary Definition',
        [Optional()]
    )


# Define the definition filler update inputs
class UpdateInputs(Base):
    definition_template_id = IntegerField(
        'Definition Template ID',
        [Optional(), NumberRange(min=1)]
    )

    filler = SelectMultipleField(
        'Definition Filler',
        [Optional()],
        choices=[]
    )

    is_dictionary = BooleanField(
        'Dictionary Definition',
        [Optional()]
    )

    is_active = BooleanField(
        'Active',
        [Optional()]
    )
