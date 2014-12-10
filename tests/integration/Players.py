import unittest
import json

from common import NoAuthTest, AuthTokenTest, get_incremental_username, \
    get_incremental_email, get_incremental_avatar_url
from application.models.Player import Player
from application.services.PlayersService import PlayersService


class NoAuthPlayersIndex(NoAuthTest):

    def test_index_returns_all_players(self):
        index_url = '/players'
        response = self.get(index_url)
        self.assertEqual(200, response.status_code)
        players = json.loads(response.data)
        self.assertEqual(self.NUM_PLAYERS, len(players))

    def test_index_returns_limited_players(self):
        index_url = '/players'
        limit = int(self.NUM_PLAYERS / 2)
        query_string = {'limit': limit}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(200, response.status_code)
        players = json.loads(response.data)
        self.assertTrue(len(players) > 0)
        self.assertEqual(limit, len(players))

    def test_index_returns_offset_players(self):
        index_url = '/players'
        offset = int(self.NUM_PLAYERS / 2)
        query_string = {'offset': offset}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(200, response.status_code)
        players = json.loads(response.data)
        self.assertEqual(self.NUM_PLAYERS - offset, len(players))

    def test_index_returns_error_from_invalid_limit(self):
        index_url = '/players'
        limit = 2.5
        query_string = {'limit': limit}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('limit'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(None, errors.get('inputs').get('limit'))

    def test_index_returns_error_from_negative_limit(self):
        index_url = '/players'
        limit = -1
        query_string = {'limit': limit}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('limit'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(limit, errors.get('inputs').get('limit'))

    def test_index_returns_error_from_invalid_offset(self):
        index_url = '/players'
        offset = 2.5
        query_string = {'offset': offset}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('offset'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(None, errors.get('inputs').get('offset'))

    def test_index_returns_error_from_negative_offset(self):
        index_url = '/players'
        offset = -1
        query_string = {'offset': offset}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('offset'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(offset, errors.get('inputs').get('offset'))


class NoAuthPlayersCreate(NoAuthTest):

    def test_create_returns_error_from_missing_username(self):
        player_id = self.NUM_PLAYERS + 1
        create_url = '/players'
        email = get_incremental_email(player_id)
        player_data = {
            'password': self.PLAYER_PASSWORD,
            'confirm': self.PLAYER_PASSWORD,
            'email': email
        }
        response = self.post(create_url, data=player_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('username'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual('', errors.get('inputs').get('username'))
        self.assertIsNone(errors.get('inputs').get('password'))
        self.assertIsNone(errors.get('inputs').get('confirm'))
        self.assertEqual(email, errors.get('inputs').get('email'))
        self.assertEqual('', errors.get('inputs').get('avatar_url'))

    def test_create_returns_error_from_long_username(self):
        player_id = self.NUM_PLAYERS + 1
        create_url = '/players'
        username = 'x' * (Player.USERNAME_MAX_LENGTH + 1)
        email = get_incremental_email(player_id)
        player_data = {
            'username': username,
            'password': self.PLAYER_PASSWORD,
            'confirm': self.PLAYER_PASSWORD,
            'email': email
        }
        response = self.post(create_url, data=player_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('username'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(username, errors.get('inputs').get('username'))
        self.assertIsNone(errors.get('inputs').get('password'))
        self.assertIsNone(errors.get('inputs').get('confirm'))
        self.assertEqual(email, errors.get('inputs').get('email'))
        self.assertEqual('', errors.get('inputs').get('avatar_url'))

    def test_create_returns_error_from_username_not_unique(self):
        player_id = self.NUM_PLAYERS + 1
        player_number = 1 if self.player.get_id() == 2 else 2
        create_url = '/players'
        username = get_incremental_username(player_number)
        email = get_incremental_email(player_id)
        player_data = {
            'username': username,
            'password': self.PLAYER_PASSWORD,
            'confirm': self.PLAYER_PASSWORD,
            'email': email
        }
        response = self.post(create_url, data=player_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('IntegrityError'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(username, errors.get('inputs').get('username'))
        self.assertIsNone(errors.get('inputs').get('password'))
        self.assertIsNone(errors.get('inputs').get('confirm'))
        self.assertEqual(email, errors.get('inputs').get('email'))
        self.assertEqual('', errors.get('inputs').get('avatar_url'))

    def test_create_returns_error_from_missing_email(self):
        player_id = self.NUM_PLAYERS + 1
        create_url = '/players'
        username = get_incremental_username(player_id)
        player_data = {
            'username': username,
            'password': self.PLAYER_PASSWORD,
            'confirm': self.PLAYER_PASSWORD
        }
        response = self.post(create_url, data=player_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('email'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(username, errors.get('inputs').get('username'))
        self.assertIsNone(errors.get('inputs').get('password'))
        self.assertIsNone(errors.get('inputs').get('confirm'))
        self.assertEqual('', errors.get('inputs').get('email'))
        self.assertEqual('', errors.get('inputs').get('avatar_url'))

    def test_create_returns_error_from_invalid_email(self):
        player_id = self.NUM_PLAYERS + 1
        create_url = '/players'
        username = get_incremental_username(player_id)
        email = get_incremental_email(player_id).replace('.', '')
        player_data = {
            'username': username,
            'password': self.PLAYER_PASSWORD,
            'confirm': self.PLAYER_PASSWORD,
            'email': email
        }
        response = self.post(create_url, data=player_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('email'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(username, errors.get('inputs').get('username'))
        self.assertIsNone(errors.get('inputs').get('password'))
        self.assertIsNone(errors.get('inputs').get('confirm'))
        self.assertEqual(email, errors.get('inputs').get('email'))
        self.assertEqual('', errors.get('inputs').get('avatar_url'))

    def test_create_returns_error_from_email_not_unique(self):
        player_id = self.NUM_PLAYERS + 1
        player_number = 1 if self.player.get_id() == 2 else 2
        create_url = '/players'
        username = get_incremental_username(player_id)
        email = get_incremental_email(player_number)
        player_data = {
            'username': username,
            'password': self.PLAYER_PASSWORD,
            'confirm': self.PLAYER_PASSWORD,
            'email': email
        }
        response = self.post(create_url, data=player_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('IntegrityError'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(username, errors.get('inputs').get('username'))
        self.assertIsNone(errors.get('inputs').get('password'))
        self.assertIsNone(errors.get('inputs').get('confirm'))
        self.assertEqual(email, errors.get('inputs').get('email'))
        self.assertEqual('', errors.get('inputs').get('avatar_url'))

    def test_create_returns_error_from_missing_password(self):
        player_id = self.NUM_PLAYERS + 1
        create_url = '/players'
        username = get_incremental_username(player_id)
        email = get_incremental_email(player_id)
        player_data = {
            'username': username,
            'confirm': self.PLAYER_PASSWORD,
            'email': email
        }
        response = self.post(create_url, data=player_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('password'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(username, errors.get('inputs').get('username'))
        self.assertIsNone(errors.get('inputs').get('password'))
        self.assertIsNone(errors.get('inputs').get('confirm'))
        self.assertEqual(email, errors.get('inputs').get('email'))
        self.assertEqual('', errors.get('inputs').get('avatar_url'))

    def test_create_returns_error_from_missing_password_confirmation(self):
        player_id = self.NUM_PLAYERS + 1
        create_url = '/players'
        username = get_incremental_username(player_id)
        email = get_incremental_email(player_id)
        player_data = {
            'username': username,
            'password': self.PLAYER_PASSWORD,
            'email': email
        }
        response = self.post(create_url, data=player_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('confirm'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(username, errors.get('inputs').get('username'))
        self.assertIsNone(errors.get('inputs').get('password'))
        self.assertIsNone(errors.get('inputs').get('confirm'))
        self.assertEqual(email, errors.get('inputs').get('email'))
        self.assertEqual('', errors.get('inputs').get('avatar_url'))

    def test_create_returns_error_from_password_confirmation_not_matching(self):
        player_id = self.NUM_PLAYERS + 1
        create_url = '/players'
        username = get_incremental_username(player_id)
        email = get_incremental_email(player_id)
        player_data = {
            'username': username,
            'password': self.PLAYER_PASSWORD,
            'confirm': 'password1',
            'email': email
        }
        response = self.post(create_url, data=player_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('password'))
        self.assertIn('must match', errors.get('errors').get('password')[0])
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(username, errors.get('inputs').get('username'))
        self.assertIsNone(errors.get('inputs').get('password'))
        self.assertIsNone(errors.get('inputs').get('confirm'))
        self.assertEqual(email, errors.get('inputs').get('email'))
        self.assertEqual('', errors.get('inputs').get('avatar_url'))

    def test_create_returns_error_from_invalid_avatar_url(self):
        player_id = self.NUM_PLAYERS + 1
        create_url = '/players'
        username = get_incremental_username(player_id)
        email = get_incremental_email(player_id)
        avatar_url = get_incremental_avatar_url(player_id).replace('.', '')
        player_data = {
            'username': username,
            'password': self.PLAYER_PASSWORD,
            'confirm': self.PLAYER_PASSWORD,
            'email': email,
            'avatar_url': avatar_url
        }
        response = self.post(create_url, data=player_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('avatar_url'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(username, errors.get('inputs').get('username'))
        self.assertIsNone(errors.get('inputs').get('password'))
        self.assertIsNone(errors.get('inputs').get('confirm'))
        self.assertEqual(email, errors.get('inputs').get('email'))
        self.assertEqual(avatar_url, errors.get('inputs').get('avatar_url'))

    def test_create_returns_created_status(self):
        player_id = self.NUM_PLAYERS + 1
        create_url = '/players'
        username = get_incremental_username(player_id)
        email = get_incremental_email(player_id)
        avatar_url = get_incremental_avatar_url(player_id)
        player_data = {
            'username': username,
            'password': self.PLAYER_PASSWORD,
            'confirm': self.PLAYER_PASSWORD,
            'email': email,
            'avatar_url': avatar_url
        }
        response = self.post(create_url, data=player_data)
        self.assertEqual(201, response.status_code)
        player = json.loads(response.data)
        self.assertIsNotNone(player.get('id'))
        self.assertIsNotNone(player.get('date_created'))
        self.assertIsNotNone(player.get('date_modified'))
        self.assertEqual(username, player.get('username'))
        self.assertEqual(email, player.get('email'))
        self.assertIsNone(player.get('password'))
        self.assertEqual(avatar_url, player.get('avatar_url'))
        self.assertEqual(True, player.get('is_active'))
        self.assertIsNotNone(player.get('auth_token'))

        # Make sure the player was actually saved to the database
        saved_player = PlayersService.get_instance().get(int(player.get('id')))
        self.assertEqual(saved_player.get_id(), player.get('id'))
        self.assertEqual(Player.dump_datetime(saved_player.get_date_created()), player.get('date_created'))
        self.assertEqual(Player.dump_datetime(saved_player.get_date_modified()), player.get('date_modified'))
        self.assertEqual(saved_player.get_username(), player.get('username'))
        self.assertEqual(saved_player.get_email(), player.get('email'))
        self.assertEqual(saved_player.get_avatar_url(), player.get('avatar_url'))
        self.assertEqual(saved_player.get_is_active(), player.get('is_active'))
        self.assertEqual(saved_player.get_auth_token(), player.get('auth_token'))


class NoAuthPlayersShow(NoAuthTest):

    def test_show_errors_without_auth(self):
        show_url = '/players/{}'.format(self.player.get_id())
        response = self.get(show_url)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('UnauthorizedAccess'))
        self.assertIsNone(errors.get('inputs'))


class AuthPlayersShow(AuthTokenTest):

    def test_show_errors_for_nonexistent_player(self):
        player_id = self.NUM_PLAYERS + 1
        show_url = '/players/{}'.format(player_id)
        response = self.get(show_url)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('PlayerNotFound'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(player_id, errors.get('inputs').get('id'))

    def test_show_returns_player(self):
        show_url = '/players/{}'.format(self.player.get_id())
        response = self.get(show_url)
        self.assertEqual(200, response.status_code)
        player = json.loads(response.data)
        self.assertEqual(self.player.get_id(), player.get('id'))
        self.assertIsNotNone(player.get('date_created'))
        self.assertIsNotNone(player.get('date_modified'))
        self.assertEqual(self.player.get_username(), player.get('username'))
        self.assertEqual(self.player.get_email(), player.get('email'))
        self.assertIsNone(player.get('password'))
        self.assertEqual(self.player.get_avatar_url(), player.get('avatar_url'))
        self.assertEqual(self.player.get_is_active(), player.get('is_active'))
        self.assertIsNone(player.get('auth_token'))


class NoAuthPlayersUpdate(NoAuthTest):

    def test_update_errors_without_auth(self):
        update_url = '/players/{}'.format(self.player.get_id())
        username = get_incremental_username(self.player.get_id())
        player_data = {
            'username': username
        }
        response = self.put(update_url, data=player_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('UnauthorizedAccess'))
        self.assertIsNone(errors.get('inputs'))


class AuthPlayersUpdate(AuthTokenTest):

    def test_update_errors_for_nonexistent_player(self):
        player_id = self.NUM_PLAYERS + 1
        update_url = '/players/{}'.format(player_id)
        username = get_incremental_username(player_id)
        player_data = {
            'username': username
        }
        response = self.put(update_url, data=player_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('PlayerNotFound'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(player_id, errors.get('inputs').get('id'))

    def test_update_returns_error_from_long_username(self):
        player_id = self.player.get_id()
        update_url = '/players/{}'.format(player_id)
        username = 'x' * (Player.USERNAME_MAX_LENGTH + 1)
        player_data = {
            'username': username
        }
        response = self.put(update_url, data=player_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('username'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(player_id, errors.get('inputs').get('id'))
        self.assertEqual(username, errors.get('inputs').get('username'))
        self.assertIsNone(errors.get('inputs').get('password'))
        self.assertEqual('', errors.get('inputs').get('email'))
        self.assertEqual('', errors.get('inputs').get('avatar_url'))

    def test_update_returns_error_from_username_not_unique(self):
        player_id = self.player.get_id()
        player_number = 1 if player_id == 2 else 2
        update_url = '/players/{}'.format(player_id)
        username = get_incremental_username(player_number)
        player_data = {
            'username': username,
        }
        response = self.put(update_url, data=player_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('IntegrityError'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(player_id, errors.get('inputs').get('id'))
        self.assertEqual(username, errors.get('inputs').get('username'))
        self.assertIsNone(errors.get('inputs').get('password'))
        self.assertEqual('', errors.get('inputs').get('email'))
        self.assertEqual('', errors.get('inputs').get('avatar_url'))

    def test_update_returns_error_from_invalid_email(self):
        player_id = self.player.get_id()
        update_url = '/players/{}'.format(player_id)
        email = get_incremental_email(player_id).replace('.', '')
        player_data = {
            'email': email
        }
        response = self.put(update_url, data=player_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('email'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(player_id, errors.get('inputs').get('id'))
        self.assertEqual('', errors.get('inputs').get('username'))
        self.assertIsNone(errors.get('inputs').get('password'))
        self.assertEqual(email, errors.get('inputs').get('email'))
        self.assertEqual('', errors.get('inputs').get('avatar_url'))

    def test_update_returns_error_from_email_not_unique(self):
        player_id = self.player.get_id()
        player_number = 1 if player_id == 2 else 2
        update_url = '/players/{}'.format(player_id)
        email = get_incremental_email(player_number)
        player_data = {
            'email': email
        }
        response = self.put(update_url, data=player_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('IntegrityError'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(player_id, errors.get('inputs').get('id'))
        self.assertEqual('', errors.get('inputs').get('username'))
        self.assertIsNone(errors.get('inputs').get('password'))
        self.assertEqual(email, errors.get('inputs').get('email'))
        self.assertEqual('', errors.get('inputs').get('avatar_url'))

    def test_update_returns_error_from_invalid_avatar_url(self):
        update_url = '/players/{}'.format(self.player.get_id())
        player_number = self.player.get_id() * 100
        avatar_url = get_incremental_avatar_url(player_number).replace('.', '')
        player_data = {
            'avatar_url': avatar_url
        }
        response = self.put(update_url, data=player_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('avatar_url'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual('', errors.get('inputs').get('username'))
        self.assertIsNone(errors.get('inputs').get('password'))
        self.assertIsNone(errors.get('inputs').get('confirm'))
        self.assertEqual('', errors.get('inputs').get('email'))
        self.assertEqual(avatar_url, errors.get('inputs').get('avatar_url'))

    def test_update_updates_player(self):
        update_url = '/players/{}'.format(self.player.get_id())
        player_number = self.player.get_id() * 100
        username = get_incremental_username(player_number)
        email = get_incremental_email(player_number)
        password = 'password{}'.format(player_number)
        avatar_url = get_incremental_avatar_url(player_number)
        player_data = {
            'username': username,
            'password': password,
            'confirm': password,
            'email': email,
            'avatar_url': avatar_url,
            'is_active': False
        }
        response = self.put(update_url, data=player_data)
        self.assertEqual(200, response.status_code)
        player = json.loads(response.data)
        self.assertIsNotNone(player.get('id'))
        self.assertIsNotNone(player.get('date_created'))
        self.assertIsNotNone(player.get('date_modified'))
        self.assertEqual(username, player.get('username'))
        self.assertEqual(email, player.get('email'))
        self.assertIsNone(player.get('password'))
        self.assertEqual(avatar_url, player.get('avatar_url'))
        self.assertEqual(False, player.get('is_active'))

        # Make sure the player was actually updated in the database
        saved_player = PlayersService.get_instance().get(int(player.get('id')))
        self.assertEqual(saved_player.get_id(), player.get('id'))
        self.assertEqual(Player.dump_datetime(saved_player.get_date_created()), player.get('date_created'))
        self.assertEqual(Player.dump_datetime(saved_player.get_date_modified()), player.get('date_modified'))
        self.assertEqual(saved_player.get_username(), player.get('username'))
        self.assertEqual(saved_player.get_email(), player.get('email'))
        self.assertEqual(saved_player.get_avatar_url(), player.get('avatar_url'))
        self.assertEqual(saved_player.get_is_active(), player.get('is_active'))


class NoAuthPlayersDelete(NoAuthTest):

    def test_delete_errors_without_auth(self):
        delete_url = '/players/{}'.format(self.player.get_id())
        response = self.delete(delete_url)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('UnauthorizedAccess'))
        self.assertIsNone(errors.get('inputs'))


class AuthPlayersDelete(AuthTokenTest):

    def test_delete_errors_for_nonexistent_player(self):
        player_id = self.NUM_PLAYERS + 1
        delete_url = '/players/{}'.format(player_id)
        response = self.delete(delete_url)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('PlayerNotFound'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(player_id, errors.get('inputs').get('id'))

    def test_delete_deletes_player(self):
        delete_url = '/players/{}'.format(self.player.get_id())
        self.assertEqual(True, self.player.get_is_active())
        response = self.delete(delete_url)
        self.assertEqual(200, response.status_code)
        player = json.loads(response.data)
        self.assertIsNotNone(player.get('id'))
        self.assertIsNotNone(player.get('date_created'))
        self.assertIsNotNone(player.get('date_modified'))
        self.assertIsNotNone(player.get('username'))
        self.assertIsNotNone(player.get('email'))
        self.assertIsNone(player.get('password'))
        self.assertEqual(False, player.get('is_active'))

        # Make sure the player was actually updated in the database
        saved_player = PlayersService.get_instance().get(int(player.get('id')))
        self.assertEqual(saved_player.get_id(), player.get('id'))
        self.assertEqual(Player.dump_datetime(saved_player.get_date_created()), player.get('date_created'))
        self.assertEqual(Player.dump_datetime(saved_player.get_date_modified()), player.get('date_modified'))
        self.assertEqual(saved_player.get_username(), player.get('username'))
        self.assertEqual(saved_player.get_email(), player.get('email'))
        self.assertEqual(saved_player.get_avatar_url(), player.get('avatar_url'))
        self.assertEqual(saved_player.get_is_active(), player.get('is_active'))


class NoAuthPlayersSignin(NoAuthTest):

    def test_signin_returns_error_from_missing_username(self):
        signin_url = '/players/signin'
        password = self.PLAYER_PASSWORD
        player_data = {
            'password': password
        }
        response = self.post(signin_url, data=player_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('username'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual('', errors.get('inputs').get('username'))
        self.assertIsNone(errors.get('inputs').get('password'))

    def test_signin_returns_error_from_nonexistent_player(self):
        signin_url = '/players/signin'
        username = self.player.get_username() * 2
        password = self.PLAYER_PASSWORD
        player_data = {
            'username': username,
            'password': password
        }
        response = self.post(signin_url, data=player_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('InvalidUsernamePassword'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(username, errors.get('inputs').get('username'))
        self.assertIsNone(errors.get('inputs').get('password'))

    def test_signin_returns_error_from_missing_password(self):
        signin_url = '/players/signin'
        username = self.player.get_username()
        player_data = {
            'username': username
        }
        response = self.post(signin_url, data=player_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('password'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(username, errors.get('inputs').get('username'))
        self.assertIsNone(errors.get('inputs').get('password'))

    def test_signin_returns_error_from_invalid_password(self):
        signin_url = '/players/signin'
        username = self.player.get_username()
        password = self.PLAYER_PASSWORD * 2
        player_data = {
            'username': username,
            'password': password
        }
        response = self.post(signin_url, data=player_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('InvalidUsernamePassword'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(username, errors.get('inputs').get('username'))
        self.assertIsNone(errors.get('inputs').get('password'))

    def test_signin_returns_error_from_inactive_user(self):
        self.player.set_is_active(False)
        self.player.save()
        signin_url = '/players/signin'
        username = self.player.get_username()
        password = self.PLAYER_PASSWORD
        player_data = {
            'username': username,
            'password': password
        }
        response = self.post(signin_url, data=player_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('SigninError'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(username, errors.get('inputs').get('username'))
        self.assertIsNone(errors.get('inputs').get('password'))

    def test_signin_signs_in_player(self):
        signin_url = '/players/signin'
        username = self.player.get_username()
        password = self.PLAYER_PASSWORD
        player_data = {
            'username': username,
            'password': password
        }
        response = self.post(signin_url, data=player_data)
        self.assertEqual(200, response.status_code)
        player = json.loads(response.data)
        self.assertEqual(self.player.get_id(), player.get('id'))
        self.assertEqual(Player.dump_datetime(self.player.get_date_created()), player.get('date_created'))
        self.assertIsNotNone(player.get('date_modified'))
        self.assertEqual(username, player.get('username'))
        self.assertEqual(self.player.get_email(), player.get('email'))
        self.assertIsNone(player.get('password'))
        self.assertEqual(self.player.get_avatar_url(), player.get('avatar_url'))
        self.assertEqual(self.player.get_is_active(), player.get('is_active'))

        # Make sure the player was actually updated in the database
        saved_player = PlayersService.get_instance().get(int(player.get('id')))
        self.assertEqual(saved_player.get_id(), player.get('id'))
        self.assertEqual(Player.dump_datetime(saved_player.get_date_created()), player.get('date_created'))
        self.assertEqual(Player.dump_datetime(saved_player.get_date_modified()), player.get('date_modified'))
        self.assertEqual(saved_player.get_username(), player.get('username'))
        self.assertEqual(saved_player.get_email(), player.get('email'))
        self.assertEqual(saved_player.get_avatar_url(), player.get('avatar_url'))
        self.assertEqual(saved_player.get_is_active(), player.get('is_active'))


class NoAuthPlayersSignout(NoAuthTest):

    def test_signout_errors_without_auth(self):
        signout_url = '/players/signout'
        response = self.post(signout_url)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('UnauthorizedAccess'))
        self.assertIsNone(errors.get('inputs'))


class AuthPlayersSignout(AuthTokenTest):

    def test_signout_signs_out_player(self):
        player_id = self.player.get_id()
        self.assertEqual(True, self.player.get_is_active())
        signout_url = '/players/signout'
        response = self.post(signout_url)
        self.assertEqual(200, response.status_code)
        player = json.loads(response.data)
        self.assertIsNotNone(player.get('Success'))

        # Make sure the player was actually updated in the database
        saved_player = PlayersService.get_instance().get(player_id)
        self.assertEqual(saved_player.get_auth_token(), None)


def main():
    unittest.main()

if __name__ == '__main__':
    main()