from application import db
from application.models.Base import Base


class Word(Base):

    __tablename__ = 'words'

    PROTECTED_ATTRIBUTES = ['lexeme_form', 'lexical_class', 'definition_templates']

    LEXEME_FORM_MAX_LENGTH = 192
    LEXICAL_CLASS_MAX_LENGTH = 32

    LEXICAL_CLASSES = ['noun', 'pronoun', 'adjective', 'verb', 'adverb', 'preposition', 'conjunction', 'interjection']

    _lexeme_form = db.Column(db.String(LEXEME_FORM_MAX_LENGTH), nullable=False, unique=True)
    _lexical_class = db.Column(db.String(LEXICAL_CLASS_MAX_LENGTH), nullable=False)
    _definition_templates = db.relationship('DefinitionTemplate', backref='_word', lazy='dynamic')
    _is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, lexeme_form, lexical_class):
        self._set_lexeme_form(lexeme_form)
        self._set_lexical_class(lexical_class)

    def get_lexeme_form(self):
        return self._lexeme_form

    def _set_lexeme_form(self, lexeme_form):
        self._lexeme_form = lexeme_form
        return self

    def get_lexical_class(self):
        return self._lexical_class

    def _set_lexical_class(self, lexical_class):
        if lexical_class not in self.LEXICAL_CLASSES:
            raise AttributeError(
                'Cannot set the lexical class to a value other than one of: {}'.format(', '.join(self.LEXICAL_CLASSES))
            )
        self._lexical_class = lexical_class
        return self

    def get_is_active(self):
        return self._is_active

    def set_is_active(self, is_active):
        self._is_active = is_active
        return self

    # Define serialized form of the model
    @property
    def serialized(self):
        base_properties = super(Word, self).serialized
        game_properties = {
            'lexeme_form': self.get_lexeme_form(),
            'lexical_class': self.get_lexical_class(),
            'is_active': self.get_is_active()
        }
        return dict(base_properties.items() + game_properties.items())
