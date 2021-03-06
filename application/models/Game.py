from application import db
from application.models.Base import Base


class Game(Base):

    __tablename__ = 'games'

    PROTECTED_ATTRIBUTES = ['match_size', 'matches', 'definition_filler_count']

    NAME_MAX_LENGTH = 128
    DESCRIPTION_MAX_LENGTH = 1024

    _name = db.Column(db.String(NAME_MAX_LENGTH), nullable=False, unique=True)
    _description = db.Column(db.String(DESCRIPTION_MAX_LENGTH), nullable=False)
    _matches = db.relationship('Match', backref='_game', lazy='dynamic')
    # Total number of players engaged in each round
    _match_size = db.Column(db.Integer, nullable=False, default=2)
    # Total number of definition fillers presented to a player every turn
    # definition_filler_count == len([dictionary_definition]) + match_size + len(auto_generated_definitions)
    _definition_filler_count = db.Column(db.Integer, nullable=False, default=4)
    _is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, name, description, match_size, definition_filler_count):
        self.set_name(name)
        self.set_description(description)
        self._set_match_size(match_size)
        self._set_definition_filler_count(definition_filler_count)

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name
        return self

    def get_description(self):
        return self._description

    def set_description(self, description):
        self._description = description
        return self

    def get_is_active(self):
        return self._is_active

    def set_is_active(self, is_active):
        self._is_active = is_active
        return self

    def get_match_size(self):
        return self._match_size

    def _set_match_size(self, match_size):
        self._match_size = match_size
        return self

    def get_definition_filler_count(self):
        return self._definition_filler_count

    def _set_definition_filler_count(self, definition_filler_count):
        self._definition_filler_count = definition_filler_count
        return self

    # Define serialized form of the model
    @property
    def serialized(self):
        base_properties = super(Game, self).serialized
        game_properties = {
            'name': self.get_name(),
            'description': self.get_description(),
            'match_size': self.get_match_size(),
            'definition_filler_count': self.get_definition_filler_count(),
            'is_active': self.get_is_active()
        }
        return dict(base_properties.items() + game_properties.items())
