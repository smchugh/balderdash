from application import db
from application.models.Base import Base
from application.models.Word import Word


class DefinitionTemplate(Base):

    __tablename__ = 'definition_templates'

    PROTECTED_ATTRIBUTES = ['definition', 'filler_lexical_classes', 'definition_fillers']

    DEFINITION_MAX_LENGTH = 512

    _word_id = db.Column(db.BigInteger, db.ForeignKey('words._id'))
    _definition = db.Column(db.String(DEFINITION_MAX_LENGTH), nullable=False)
    _filler_lexical_classes = db.Column(db.PickleType(), nullable=False)
    _definition_fillers = db.relationship('DefinitionFiller', backref='definition_template', lazy='dynamic')
    _is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, word, definition, filler_lexical_classes):
        self.word = word
        self._set_definition(definition)
        self._set_filler_lexical_classes(filler_lexical_classes)

    def __repr__(self):
        return '<DefinitionTemplate %r>' % self.get_id()

    def get_word(self):
        return self.word

    def get_definition(self):
        return self._definition

    def _set_definition(self, definition):
        self._definition = definition
        return self

    def get_filler_lexical_classes(self):
        return self._filler_lexical_classes

    def _set_filler_lexical_classes(self, filler_lexical_classes):
        filler_lexical_classes = filler_lexical_classes if filler_lexical_classes is not None else list()

        if not isinstance(filler_lexical_classes, list):
            raise AttributeError('The filler lexical classes must be a list.')

        if len(filler_lexical_classes) != self.get_definition().count('{}'):
            raise AttributeError(
                'There are {} filler lexical classes but {} fillers. These values must be the same.'.format(
                    len(filler_lexical_classes),
                    self.get_definition().count('{}')
                )
            )

        if any(lexical_class not in Word.LEXICAL_CLASSES for lexical_class in filler_lexical_classes):
            raise AttributeError(
                'Cannot set the filler lexical classes to a value other than one of: {}'.format(
                    ', '.join(Word.LEXICAL_CLASSES)
                )
            )

        self._filler_lexical_classes = filler_lexical_classes
        return self

    def get_is_active(self):
        return self._is_active

    def set_is_active(self, is_active):
        self._is_active = is_active
        return self

    # Define serialized form of the model
    @property
    def serialized(self):
        base_properties = super(DefinitionTemplate, self).serialized
        game_properties = {
            'word': self.get_word().serialized,
            'definition': self.get_definition(),
            'filler_lexical_classes': self.get_filler_lexical_classes(),
            'is_active': self.get_is_active()
        }
        return dict(base_properties.items() + game_properties.items())

    @classmethod
    def get_list_by_word(cls, word_id, limit, offset):
        return cls.get_list_query(limit, offset).filter(
            cls._word_id == word_id
        ).all()
