from application import db
from application.models.Base import Base


class Turn(Base):

    __tablename__ = 'turns'

    PROTECTED_ATTRIBUTES = ['match_id', 'match', 'word_id', 'word']

    STATE_SUPPLYING = (0, 'supplying')
    STATE_SELECTING = (1, 'selecting')
    STATE_CANCELED = (2, 'canceled')
    STATE_COMPLETED = (3, 'completed')
    STATES = [STATE_SUPPLYING, STATE_SELECTING, STATE_CANCELED, STATE_COMPLETED]

    _match_id = db.Column(db.BigInteger, db.ForeignKey('matches._id'), nullable=False)
    _players = db.relationship('TurnPlayer', backref='_turn', lazy='dynamic')
    _word_id = db.Column(db.BigInteger, db.ForeignKey('words._id'), nullable=False)
    _state = db.Column(db.SmallInteger, default=STATE_SUPPLYING[0], nullable=False)
    _date_canceled = db.Column(db.DateTime)
    _date_completed = db.Column(db.DateTime)

    def __init__(self, match, player, word):
        self._set_match(match)
        self._set_player(player)
        self._set_word(word)

    def get_match(self):
        return self._match

    def _set_match(self, match):
        self._match = match
        return self

    def get_player(self):
        return self._player

    def _set_player(self, player):
        self._player = player
        return self

    def get_word(self):
        return self._word

    def _set_word(self, word):
        self._word = word
        return self

    def get_state(self):
        return self._state

    def get_state_string(self):
        return self.STATES[self.get_state()][1]

    def _set_state(self, state_id):
        if state_id not in [state[0] for state in self.STATES]:
            raise AttributeError(
                'Cannot set the state to a value other than one of: {}'.format(
                    ', '.join([state[1] for state in self.STATES])
                )
            )
        self._state = state_id
        return self

    def get_date_started(self):
        return self._date_started

    def _set_date_started(self, date_started):
        self._date_started = date_started
        return self

    def get_date_canceled(self):
        return self._date_canceled

    def _set_date_canceled(self, date_canceled):
        self._date_canceled = date_canceled
        return self

    def get_date_completed(self):
        return self._date_completed

    def _set_date_completed(self, date_completed):
        self._date_completed = date_completed
        return self

    # Define serialized form of the model
    @property
    def serialized(self):
        base_properties = super(Turn, self).serialized
        turn_properties = {
            'player': self.get_player(),
            'match': self.get_match(),
            'word': self.get_word(),
            'opponents': self.get_opponents()
        }
        return dict(base_properties.items() + turn_properties.items())
