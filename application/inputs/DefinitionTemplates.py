# Import input types such as TextField
from wtforms import StringField, IntegerField, BooleanField, SelectMultipleField

# Import input validators
from wtforms.validators import InputRequired, Length, NumberRange, Optional

# Import Base inputs class
from application.inputs.Base import Base

# Import the Definition Template and Word models
from application.models.DefinitionTemplate import DefinitionTemplate
from application.models.Word import Word


# Define the definition template list inputs
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


# Define the definition template creation inputs
class CreateInputs(Base):
    word_id = IntegerField(
        'Word ID',
        [
            InputRequired(message='Must provide the word ID'),
            NumberRange(min=1)
        ]
    )

    definition = StringField(
        'Definitions',
        [
            InputRequired(message='Must provide the definition of the word'),
            Length(
                max=DefinitionTemplate.DEFINITION_MAX_LENGTH,
                message='The definition can not be more than {} characters'.format(
                    DefinitionTemplate.DEFINITION_MAX_LENGTH
                )
            )
        ]
    )

    filler_lexical_classes = SelectMultipleField(
        'Filler Lexical Classes',
        [InputRequired(message='Must provide the lexical classes for the definition filler')],
        choices=[(lexical_class, lexical_class) for lexical_class in Word.LEXICAL_CLASSES]
    )


# Define the definition template update inputs
class UpdateInputs(Base):
    word_id = IntegerField(
        'Word ID',
        [
            Optional(),
            NumberRange(min=1)
        ]
    )

    definition = StringField(
        'Definitions',
        [
            Optional(),
            Length(
                max=DefinitionTemplate.DEFINITION_MAX_LENGTH,
                message='The definition can not be more than {} characters'.format(
                    DefinitionTemplate.DEFINITION_MAX_LENGTH
                )
            )
        ]
    )

    filler_lexical_classes = SelectMultipleField(
        'Filler Lexical Classes',
        [Optional()],
        choices=[(lexical_class, lexical_class) for lexical_class in Word.LEXICAL_CLASSES]
    )

    is_active = BooleanField(
        'Active',
        [Optional()]
    )
