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

    PROTECTED_ATTRIBUTES = ['game_id', 'date_started', 'date_canceled', 'date_completed', 'players']

    STATE_WAITING = 1
    STATE_STARTED = 2
    STATE_CANCELED = 3
    STATE_COMPLETED = 4

    _game_id = db.Column(db.BigInteger, db.ForeignKey('games._id'))
    _players = db.relationship(
        'Player',
        secondary=match_players,
        backref=db.backref('matches', lazy='dynamic'),
        order_by=match_players.c.player_id
    )
    _state = db.Column(db.SmallInteger, default=STATE_WAITING)
    _date_started = db.Column(db.DateTime)
    _date_canceled = db.Column(db.DateTime)
    _date_completed = db.Column(db.DateTime)

    def __init__(self, game_id, player):
        self._game_id = game_id
        self.add_player(player)

    def __repr__(self):
        return '<Match %r>' % self._id

    def start(self):
        self._date_started = db.func.current_timestamp()
        self._state = self.STATE_STARTED
        return self

    def cancel(self):
        self._date_canceled = db.func.current_timestamp()
        self._state = self.STATE_CANCELED
        return self

    def complete(self):
        self._date_completed = db.func.current_timestamp()
        self._state = self.STATE_COMPLETED
        return self

    def add_player(self, player, should_start=True):
        self._players.append(player)

        if should_start and len(self._players) == self.game.get_match_size():
            self.start()

        return self

    # Define serialized form of the model
    @property
    def serialized(self):
        base_properties = super(Match, self).serialized
        match_properties = {
            'date_started': self.dump_datetime(self._date_started),
            'date_canceled': self.dump_datetime(self._date_canceled),
            'date_completed': self.dump_datetime(self._date_completed),
            'game': self.game.serialized,
            'players': {player.get_id(): player.serialized for player in self._players}
        }

        # TODO if date_started != None and date_canceled == None and date_completed == None, show the
        # turn info (from turn endpoint or match ?)

        return dict(base_properties.items() + match_properties.items())

    @classmethod
    def get_list_by_game_for_player(cls, game_id, player_id, limit, offset):
        return cls.get_list_query(limit, offset).filter(
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
