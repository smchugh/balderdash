import os


class BaseConfig(object):
    USERNAME_MAX_LENGTH = 128
    EMAIL_MAX_LENGTH = 128
    PASSWORD_MAX_LENGTH = 192
    AUTH_TOKEN_LENGTH = 128
    AVATAR_URL_MAX_LENGTH = 256
    GAME_NAME_MAX_LENGTH = 128
    GAME_DESCRIPTION_MAX_LENGTH = 1024


class DevConfig(BaseConfig):
    pass


class StagingConfig(BaseConfig):
    pass


class ProdConfig(BaseConfig):
    pass


APPLICATION_ENV = os.environ.get('APPLICATION_ENV', 'dev')
settings = None

if APPLICATION_ENV == 'dev':
    settings = DevConfig()
elif APPLICATION_ENV == 'staging':
    settings = StagingConfig()
elif APPLICATION_ENV == 'production':
    settings = ProdConfig()