from application import db
from application.models.Base import Base
from application.models.Game import Game

# Define the many-to-many join table for the players assigned to a particular match
match_players = db.Table(
    'match_players',
    Base.metadata,
    db.Column('match_id', db.BigInteger, db.ForeignKey('matches._id')),
    db.Column('player_id', db.BigInteger, db.ForeignKey('players._id')),
    db.Column('date_joined', db.DateTime, default=db.func.current_timestamp())
)


class Match(Base):

    __tablename__ = 'matches'

    PROTECTED_ATTRIBUTES = ['game_id', 'date_started', 'date_canceled', 'date_completed', 'players', 'state', 'game']

    STATE_WAITING = (0, 'waiting')
    STATE_STARTED = (1, 'stared')
    STATE_CANCELED = (2, 'canceled')
    STATE_COMPLETED = (3, 'completed')
    STATES = [STATE_WAITING, STATE_STARTED, STATE_CANCELED, STATE_COMPLETED]

    _game_id = db.Column(db.BigInteger, db.ForeignKey('games._id'), nullable=False)
    _players = db.relationship(
        'Player',
        secondary=match_players,
        backref=db.backref('_matches', lazy='dynamic'),
        order_by=match_players.c.player_id
    )
    _state = db.Column(db.SmallInteger, default=STATE_WAITING[0], nullable=False)
    _date_started = db.Column(db.DateTime)
    _date_canceled = db.Column(db.DateTime)
    _date_completed = db.Column(db.DateTime)
    _is_archived = db.Column(db.Boolean, default=False)
    _is_hidden = db.Column(db.Boolean, default=False)

    def __init__(self, game, player):
        self._set_game(game)
        self.add_player(player)

    def __repr__(self):
        return '<Match %r>' % self.get_id()

    def get_game(self):
        if self._game is None:
            raise AttributeError(
                'Match {} does not have a game. All matches must be assigned a game.'.format(self.get_id())
            )
        return self._game

    def _set_game(self, game):
        self._game = game
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

    def get_is_archived(self):
        return self._is_archived

    def set_is_archived(self, is_archived):
        self._is_archived = is_archived

    def get_is_hidden(self):
        return self._is_hidden

    def set_is_hidden(self, is_hidden):
        self._is_hidden = is_hidden

    def start(self):
        self._set_date_started(db.func.current_timestamp())
        self._set_state(self.STATE_STARTED[0])
        return self

    def cancel(self):
        self._set_date_canceled(db.func.current_timestamp())
        self._set_state(self.STATE_CANCELED[0])
        return self

    def complete(self):
        self._set_date_completed(db.func.current_timestamp())
        self._set_state(self.STATE_COMPLETED[0])
        return self

    def get_players(self):
        return [] if self._players is None else self._players

    def add_player(self, player, should_start=True):
        self._players.append(player)

        if should_start and len(self.get_players()) == self.get_game().get_match_size():
            self.start()

        return self

    # Define serialized form of the model
    @property
    def serialized(self):
        base_properties = super(Match, self).serialized
        match_properties = {
            'date_started': self.dump_datetime(self.get_date_started()),
            'date_canceled': self.dump_datetime(self.get_date_canceled()),
            'date_completed': self.dump_datetime(self.get_date_completed()),
            'game': self.get_game().serialized,
            'players': {player.get_id(): player.serialized for player in self.get_players()}
        }

        # TODO if date_started != None and date_canceled == None and date_completed == None, show the
        # turn info (from turn endpoint or match ?)

        return dict(base_properties.items() + match_properties.items())

    @classmethod
    def get_list_by_game_for_player(cls, game_id, player_id, limit, offset):
        return cls.get_list_query(limit, offset).join(
            match_players
        ).filter(
            match_players.c.player_id == player_id,
            cls._game_id == game_id
        ).all()

    @classmethod
    def get_opponent_match(cls, game_id, player, opponent_id):
        # TODO return only the matches for this game with null start and cancel dates as a subquery before joining

        return cls.query.join(
            match_players
        ).filter(
            cls._game_id == game_id,
            cls._date_started == None,
            cls._date_canceled == None,
            match_players.c.player_id == opponent_id,
            # TODO replace with sqlalchemy subquery
            '{} NOT IN (SELECT player_id FROM match_players WHERE match_players.match_id = matches._id)'.format(
                player.get_id()
            )
        ).order_by(
            cls._date_created.asc()
        ).with_for_update().first()

    @classmethod
    def get_random_match(cls, game_id, player):
        return cls.query.join(
            match_players, Game
        ).filter(
            cls._game_id == game_id,
            cls._date_started == None,
            cls._date_canceled == None,
            # TODO replace with sqlalchemy subquery
            '{} NOT IN (SELECT player_id FROM match_players WHERE match_players.match_id = matches._id)'.format(
                player.get_id()
            ),
            # TODO replace with sqlalchemy subquery
            'games._match_size > (SELECT COUNT(*) FROM match_players WHERE match_players.match_id = matches._id)'
        ).order_by(
            cls._date_created.asc()
        ).with_for_update().first()
