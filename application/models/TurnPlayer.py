from application import db
from application.models.Base import Base


class TurnPlayer(Base):

    __tablename__ = 'turn_player'

    PROTECTED_ATTRIBUTES = ['turn_id', 'turn', 'player_id', 'player', 'is_selector']

    _turn_id = db.Column(db.BigInteger, db.ForeignKey('turns._id'), nullable=False)
    _player_id = db.Column(db.BigInteger, db.ForeignKey('players._id'))
    # True if this is the player selecting a definition filler this turn
    _is_selector = db.Column(db.Boolean, nullable=False, default=False)
    # This players score from this turn
    _score = db.Column(db.Integer, nullable=False, default=0)
    # True if this player has seen the replay for this turn
    _viewed_replay = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, turn, player, is_selector=False):
        self._set_turn(turn)
        self._set_player(player)
        self._set_is_selectorr(is_selector)

    def get_turn(self):
        return self.turn

    def get_turn_id(self):
        return self._turn_id

    def _set_turn(self, turn):
        self.turn = turn
        return self

    def get_player(self):
        return self.player

    def get_player_id(self):
        return self._player_id

    def _set_player(self, player):
        self.player = player
        return self

    def get_is_selector(self):
        return self._is_selector

    def _set_is_selector(self, is_selector):
        self._is_selector = is_selector
        return self

    def get_score(self):
        return self._score

    def set_score(self, score):
        self._score = score
        return self

    def get_viewed_replay(self):
        return self._viewed_replay

    def _set_viewed_replay(self, viewed_replay):
        self._viewed_replay = viewed_replay
        return self

    # Define serialized form of the model
    @property
    def serialized(self):
        base_properties = super(TurnPlayer, self).serialized
        turn_player_properties = {
            'turn_id': self.get_turn_id(),
            'player_id': self.get_player_id(),
            'is_selector': self.get_is_selector(),
            'score': self.get_score(),
            'viewed_replay': self.get_viewed_replay()
        }
        return dict(base_properties.items() + turn_player_properties.items())
