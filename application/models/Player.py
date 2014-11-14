from application import db
from application.models.Base import Base

# Import global app settings
from settings import settings


class Player(Base):

    __tablename__ = 'players'

    _username = db.Column(db.String(settings.USERNAME_MAX_LENGTH), nullable=False, unique=True)
    _password = db.Column(db.String(settings.PASSWORD_MAX_LENGTH), nullable=False)
    _is_active = db.Column(db.Boolean(), nullable=False, default=True)

    def __init__(self, username, password):
        self._username = username
        self._password = password

    def __repr__(self):
        return '<Player %r>' % self._id

    def get_password(self):
        return self._password

    # Four methods for flask-login
    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def is_active(self):
        return self._is_active

    def get_id(self):
        try:
            return unicode(self._id)  # python 2
        except NameError:
            return str(self._id)  # python 3

    # Define serialized form of the model
    @property
    def serialized(self):
        base_properties = super(Player, self).serialized
        player_properties = {
            'username': self._username,
            'is_active': self.is_active()
        }
        return dict(base_properties.items() + player_properties.items())
