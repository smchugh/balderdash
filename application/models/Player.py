from application import db
from application.models.Base import Base
from settings import settings


class Player(Base):

    __tablename__ = 'players'

    username = db.Column(db.String(settings.USERNAME_MAX_LENGTH), nullable=False, unique=True)
    password = db.Column(db.String(settings.PASSWORD_MAX_LENGTH), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<Player %r>' % self.id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def is_active(self):
        return self.active

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    @property
    def serialized(self):
        base_properties = super(Player, self).serialized
        player_properties = {
            'username': self.username,
            'is_active': self.is_active()
        }
        return dict(base_properties.items() + player_properties.items())
