import os


class BaseConfig(object):
    USERNAME_MAX_LENGTH = 128
    PASSWORD_MAX_LENGTH = 192


class DevConfig(BaseConfig):
    pass


class StagingConfig(BaseConfig):
    pass


class ProdConfig(BaseConfig):
    pass


APPLICATION_ENV = os.environ.get('APPLICATION_ENV', 'dev')
settings = None

# logging.error("application env: {}".format(APPLICATION_ENV))
if APPLICATION_ENV == 'dev':
    settings = DevConfig()
elif APPLICATION_ENV == 'staging':
    settings = StagingConfig()
elif APPLICATION_ENV == 'production':
    settings = ProdConfig()