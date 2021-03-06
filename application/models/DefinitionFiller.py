from application import db
from application.models.Base import Base
from application.models.DefinitionTemplate import DefinitionTemplate


class DefinitionFiller(Base):

    __tablename__ = 'definition_fillers'

    PROTECTED_ATTRIBUTES = ['definition_template_id', 'definition_template', 'filler', 'is_dictionary']

    _definition_template_id = db.Column(db.BigInteger, db.ForeignKey('definition_templates._id'), nullable=False)
    _filler = db.Column(db.PickleType(), nullable=False)
    _is_dictionary = db.Column(db.Boolean, nullable=False, default=False)
    _is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, definition_template, filler, is_dictionary):
        self._set_definition_template(definition_template)
        self._set_filler(filler)
        self._set_is_dictionary(is_dictionary)

    def get_definition_template(self):
        return self._definition_template

    def _set_definition_template(self, definition_template):
        self._definition_template = definition_template
        return self

    def get_filler(self):
        return self._filler

    def _set_filler(self, filler):
        filler = filler if filler is not None else list()

        if not isinstance(filler, list):
            raise AttributeError('The filler must be a list.')

        if not isinstance(self.get_definition_template(), DefinitionTemplate):
            raise AttributeError('The definition filler must be assigned to a definition template')

        if len(filler) != len(self.get_definition_template().get_filler_lexical_classes()):
            raise AttributeError(
                'There are {} filler but {} filler lexical classes. These values must be the same.'.format(
                    len(filler),
                    len(self.get_definition_template().get_filler_lexical_classes())
                )
            )

        self._filler = filler
        return self

    def get_is_dictionary(self):
        return self._is_dictionary

    def _set_is_dictionary(self, is_dictionary):
        self._is_dictionary = is_dictionary
        return self

    def get_is_active(self):
        return self._is_active

    def set_is_active(self, is_active):
        self._is_active = is_active
        return self

    def save(self):
        # TODO Add check that only one filler is the dictionary definition
        super(DefinitionFiller, self).save()

    # Define serialized form of the model
    @property
    def serialized(self):
        base_properties = super(DefinitionFiller, self).serialized
        definition_filler_properties = {
            'definition_template': self.get_definition_template().serialized,
            'filler': self.get_filler(),
            'is_dictionary': self.get_is_dictionary(),
            'is_active': self.get_is_active()
        }
        return dict(base_properties.items() + definition_filler_properties.items())
