import json

from tests.TestCase import TestCase
from application import app
from application.models.Player import Player


def get_incremental_username(increment):
    return 'player_{}'.format(increment)


def get_incremental_email(increment):
    return '{}@test.com'.format(get_incremental_username(increment))


def get_incremental_avatar_url(increment):
    return 'http://cdn.balderdash.com/avatars/{}.jpg'.format(get_incremental_username(increment))


class NoAuthTest(TestCase):
    NUM_PLAYERS = 11
    PLAYER_PASSWORD = 'password'

    def setUp(self):
        super(NoAuthTest, self).setUp()
        self.client = app.test_client()
        self.headers = {'Content-Type': 'application/json', 'charset': 'utf-8'}
        self.params = {}

    def insert_dummy_data(self):
        super(NoAuthTest, self).insert_dummy_data()

        player = None
        for player_index in range(1, self.NUM_PLAYERS + 1):
            username = get_incremental_username(player_index)
            email = get_incremental_email(player_index)
            avatar_url = get_incremental_avatar_url(player_index) if player_index % 2 == 0 else None
            player = Player(username, self.PLAYER_PASSWORD, email, avatar_url)
            player.save()

        self.player = player

    def get_params(self, request_params=None):
        params = self.params
        if request_params and isinstance(request_params, dict):
            params = dict(params.items() + request_params.items())

        return params

    def get_data(self, request_params=None):
        params = self.get_params(request_params)
        return json.dumps(params)

    def get_headers(self, request_headers=None):
        headers = self.headers
        if request_headers and isinstance(request_headers, dict):
            headers = dict(headers.items() + request_headers.items())

        return headers

    def get(self, *args, **kwargs):
        kwargs['query_string'] = self.get_params(kwargs.get('query_string'))
        kwargs['headers'] = self.get_headers(kwargs.get('headers'))
        return self.client.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        kwargs['data'] = self.get_data(kwargs.get('data'))
        kwargs['headers'] = self.get_headers(kwargs.get('headers'))
        return self.client.post(*args, **kwargs)

    def put(self, *args, **kwargs):
        kwargs['data'] = self.get_data(kwargs.get('data'))
        kwargs['headers'] = self.get_headers(kwargs.get('headers'))
        return self.client.put(*args, **kwargs)

    def delete(self, *args, **kwargs):
        kwargs['data'] = self.get_data(kwargs.get('data'))
        kwargs['headers'] = self.get_headers(kwargs.get('headers'))
        return self.client.delete(*args, **kwargs)


class AuthTokenTest(NoAuthTest):
    def setUp(self):
        super(AuthTokenTest, self).setUp()
        self.assertIsNotNone(self.player)
        self.player.login()

        # Add auth token to params
        self.params = self.get_params({'auth_token': self.player.get_auth_token()})
