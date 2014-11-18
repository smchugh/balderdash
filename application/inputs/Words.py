# Import input types such as TextField
from wtforms import StringField, IntegerField, BooleanField

# Import input validators
from wtforms.validators import InputRequired, Length, NumberRange, Optional, AnyOf

# Import Base inputs class
from application.inputs.Base import Base

# Import the Word model
from application.models.Word import Word


# Define the word list inputs
class ListInputs(Base):
    offset = IntegerField(
        'Offset',
        [Optional(), NumberRange(min=0)]
    )

    limit = IntegerField(
        'Limit',
        [Optional(), NumberRange(min=0)]
    )


# Define the word creation inputs
class CreateInputs(Base):
    lexeme_form = StringField(
        'Lexeme Form',
        [
            InputRequired(message='Must provide a lexeme form of the word'),
            Length(
                max=Word.LEXEME_FORM_MAX_LENGTH,
                message='The lexeme form can not be more than {} characters'.format(Word.LEXEME_FORM_MAX_LENGTH)
            )
        ]
    )

    lexical_class = StringField(
        'Lexical Class',
        [
            InputRequired(message='Must provide the lexical class of the word'),
            AnyOf(
                values=Word.LEXICAL_CLASSES,
                message='The lexical class must be one of: {}'.format(', '.join(Word.LEXICAL_CLASSES))
            )
        ]
    )


# Define the word update inputs
class UpdateInputs(Base):
    lexeme_form = StringField(
        'Lexeme Form',
        [
            Optional(),
            Length(
                max=Word.LEXEME_FORM_MAX_LENGTH,
                message='The lexeme form can not be more than {} characters'.format(Word.LEXEME_FORM_MAX_LENGTH)
            )
        ]
    )

    lexical_class = StringField(
        'Lexical Class',
        [
            Optional(),
            AnyOf(
                values=Word.LEXICAL_CLASSES,
                message='The lexical class must be one of: {}'.format(', '.join(Word.LEXICAL_CLASSES))
            )
        ]
    )

    is_active = BooleanField(
        'Active',
        [Optional()]
    )


