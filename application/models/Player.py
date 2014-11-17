import uuid

from application import db, app
from application.models.Base import Base


class Player(Base):

    __tablename__ = 'players'

    PROTECTED_ATTRIBUTES = ['auth_token']

    USERNAME_MAX_LENGTH = 128
    EMAIL_MAX_LENGTH = 128
    PASSWORD_MAX_LENGTH = 192
    AUTH_TOKEN_LENGTH = 128
    AVATAR_URL_MAX_LENGTH = 256

    _username = db.Column(db.String(USERNAME_MAX_LENGTH), nullable=False, unique=True)
    _email = db.Column(db.String(EMAIL_MAX_LENGTH), nullable=False, unique=True)
    _password = db.Column(db.String(PASSWORD_MAX_LENGTH), nullable=False)
    _is_active = db.Column(db.Boolean(), nullable=False, default=True)
    _auth_token = db.Column(db.String(AUTH_TOKEN_LENGTH))
    _avatar_url = db.Column(db.String(AVATAR_URL_MAX_LENGTH))

    def __init__(self, username, password):
        self._username = username
        self._password = password

    def __repr__(self):
        return '<Player %r>' % self._id

    def get_password(self):
        return self._password

    def is_active(self):
        return self._is_active

    def set_auth_token(self, auth_token):
        self._auth_token = auth_token

    def get_auth_token(self):
        return self._auth_token

    def login(self):
        if not self.is_active():
            return False

        auth_token = uuid.uuid4()
        self.set_auth_token(auth_token)

        try:
            self.save()
        except Exception as e:
            app.logger.error('Failed to save auth token with error: {}'.format(e.message))
            return False

        return True

    def logout(self):
        self.set_auth_token(None)

        try:
            self.save()
        except Exception as e:
            app.logger.error('Failed to remove auth token with error: {}'.format(e.message))
            return False

    # Define serialized form of the model
    @property
    def serialized(self):
        base_properties = super(Player, self).serialized
        player_properties = {
            'username': self._username,
            'is_active': self.is_active()
        }
        return dict(base_properties.items() + player_properties.items())

    @classmethod
    def get_from_auth(cls, auth_token):
        return cls.query.filter_by(_auth_token=auth_token).first()
