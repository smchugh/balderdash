from application import db
from application.models.Base import Base

# Import global app settings
from settings import settings


class Game(Base):

    __tablename__ = 'games'

    PROTECTED_ATTRIBUTES = ['match_size', 'matches']

    _name = db.Column(db.String(settings.GAME_NAME_MAX_LENGTH), nullable=False, unique=True)
    _description = db.Column(db.String(settings.GAME_DESCRIPTION_MAX_LENGTH), nullable=False)
    _matches = db.relationship('Match', backref='game', lazy='dynamic')
    _match_size = db.Column(db.Integer, nullable=False, default=2)
    _is_active = db.Column(db.Boolean(), nullable=False, default=True)

    def __init__(self, name, description):
        self._name = name
        self._description = description

    def __repr__(self):
        return '<Game %r>' % self._id

    def get_match_size(self):
        return self._match_size

    # Define serialized form of the model
    @property
    def serialized(self):
        base_properties = super(Game, self).serialized
        game_properties = {
            'name': self._name,
            'description': self._description,
            'match_size': self._match_size,
            'is_active': self._is_active
        }
        return dict(base_properties.items() + game_properties.items())
