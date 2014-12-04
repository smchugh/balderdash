import os

environment = os.environ.get('APPLICATION_ENV', 'development')
env_config = 'config.{}'.format(environment)


def env_bool(env_param, default=False):
    return str(os.environ.get(env_param, default)).lower() in ['true', '1', 'y', 'yes']