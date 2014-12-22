import uuid

from werkzeug.security import generate_password_hash

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
    FB_ID_MAX_LENGTH = 128

    _username = db.Column(db.String(USERNAME_MAX_LENGTH), nullable=False, unique=True)
    _email = db.Column(db.String(EMAIL_MAX_LENGTH), nullable=False, unique=True)
    _password = db.Column(db.String(PASSWORD_MAX_LENGTH), nullable=False)
    _is_active = db.Column(db.Boolean, nullable=False, default=True)
    _auth_token = db.Column(db.String(AUTH_TOKEN_LENGTH))
    _avatar_url = db.Column(db.String(AVATAR_URL_MAX_LENGTH))
    _facebook_id = db.Column(db.String(FB_ID_MAX_LENGTH))

    def __init__(self, username, password, email, avatar_url, facebook_id=None):
        self.set_username(username)
        self.set_password(password)
        self.set_email(email)
        self.set_avatar_url(avatar_url)
        self._set_auth_token(self.generate_auth_token())
        self.set_facebook_id(facebook_id)

    def get_username(self):
        return self._username

    def set_username(self, username):
        self._username = username
        return self

    def get_email(self):
        return self._email

    def set_email(self, email):
        self._email = email
        return self

    def get_password(self):
        return self._password

    def set_password(self, password):
        self._password = generate_password_hash(password)
        return self

    def get_is_active(self):
        return self._is_active

    def set_is_active(self, is_active):
        self._is_active = is_active
        return self

    def get_auth_token(self):
        return self._auth_token

    def _set_auth_token(self, auth_token):
        self._auth_token = auth_token
        return self

    def get_avatar_url(self):
        return self._avatar_url

    def set_avatar_url(self, avatar_url):
        self._avatar_url = avatar_url
        return self

    def get_facebook_id(self):
        return self._facebook_id

    def set_facebook_id(self, facebook_id):
        self._facebook_id = facebook_id
        return self

    def login(self):
        if not self.get_is_active():
            return False

        self._set_auth_token(self.generate_auth_token())

        try:
            self.save()
        except Exception as e:
            app.logger.error('Failed to save auth token with error: {}'.format(e.message))
            return False

        return True

    def logout(self):
        self._set_auth_token(None)

        try:
            self.save()
        except Exception as e:
            app.logger.error('Failed to remove auth token with error: {}'.format(e.message))
            return False

        return True

    # Define serialized form of the model
    @property
    def serialized(self):
        base_properties = super(Player, self).serialized
        player_properties = {
            'username': self.get_username(),
            'email': self.get_email(),
            'avatar_url': self.get_avatar_url(),
            'is_active': self.get_is_active(),
            'facebook_id': self.get_facebook_id()
        }
        return dict(base_properties.items() + player_properties.items())

    @staticmethod
    def generate_auth_token():
        return uuid.uuid4()
