import unittest
import json

from common import NoAuthTest, get_incremental_game_name, get_incremental_game_description
from application.models.Game import Game
from application.services.GamesService import GamesService


class GamesIndex(NoAuthTest):

    def test_index_returns_all_games(self):
        index_url = '/games'
        response = self.get(index_url)
        self.assertEqual(200, response.status_code)
        games = json.loads(response.data)
        self.assertEqual(self.NUM_GAMES, len(games))

    def test_index_returns_limited_games(self):
        index_url = '/games'
        limit = int(self.NUM_GAMES / 2)
        query_string = {'limit': limit}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(200, response.status_code)
        games = json.loads(response.data)
        self.assertTrue(len(games) > 0)
        self.assertEqual(limit, len(games))

    def test_index_returns_offset_games(self):
        index_url = '/games'
        offset = int(self.NUM_GAMES / 2)
        query_string = {'offset': offset}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(200, response.status_code)
        games = json.loads(response.data)
        self.assertEqual(self.NUM_GAMES - offset, len(games))

    def test_index_returns_error_from_invalid_limit(self):
        index_url = '/games'
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
        index_url = '/games'
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
        index_url = '/games'
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
        index_url = '/games'
        offset = -1
        query_string = {'offset': offset}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('offset'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(offset, errors.get('inputs').get('offset'))


class GamesCreate(NoAuthTest):

    def test_create_returns_error_from_missing_name(self):
        game_id = self.NUM_GAMES + 1
        create_url = '/games'
        description = get_incremental_game_description(game_id)
        game_data = {
            'description': description,
            'match_size': 2
        }
        response = self.post(create_url, data=game_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('name'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual('', errors.get('inputs').get('name'))
        self.assertEqual(description, errors.get('inputs').get('description'))
        self.assertEqual(2, errors.get('inputs').get('match_size'))

    def test_create_returns_error_from_long_name(self):
        game_id = self.NUM_GAMES + 1
        create_url = '/games'
        name = 'x' * (Game.NAME_MAX_LENGTH + 1)
        description = get_incremental_game_description(game_id)
        game_data = {
            'name': name,
            'description': description,
            'match_size': 2
        }
        response = self.post(create_url, data=game_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('name'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(name, errors.get('inputs').get('name'))
        self.assertEqual(description, errors.get('inputs').get('description'))
        self.assertEqual(2, errors.get('inputs').get('match_size'))

    def test_create_returns_error_from_name_not_unique(self):
        game_id = self.NUM_GAMES + 1
        game_number = 1 if self.game.get_id() == 2 else 2
        create_url = '/games'
        name = get_incremental_game_name(game_number)
        description = get_incremental_game_description(game_id)
        game_data = {
            'name': name,
            'description': description,
            'match_size': 2
        }
        response = self.post(create_url, data=game_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('IntegrityError'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(name, errors.get('inputs').get('name'))
        self.assertEqual(description, errors.get('inputs').get('description'))
        self.assertEqual(2, errors.get('inputs').get('match_size'))

    def test_create_returns_error_from_missing_description(self):
        game_id = self.NUM_GAMES + 1
        create_url = '/games'
        name = get_incremental_game_name(game_id)
        game_data = {
            'name': name,
            'match_size': 2
        }
        response = self.post(create_url, data=game_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('description'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(name, errors.get('inputs').get('name'))
        self.assertEqual('', errors.get('inputs').get('description'))
        self.assertEqual(2, errors.get('inputs').get('match_size'))

    def test_create_returns_error_from_long_description(self):
        game_id = self.NUM_GAMES + 1
        create_url = '/games'
        name = get_incremental_game_name(game_id)
        description = 'x' * (Game.DESCRIPTION_MAX_LENGTH+ 1)
        game_data = {
            'name': name,
            'description': description,
            'match_size': 2
        }
        response = self.post(create_url, data=game_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('description'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(name, errors.get('inputs').get('name'))
        self.assertEqual(description, errors.get('inputs').get('description'))
        self.assertEqual(2, errors.get('inputs').get('match_size'))

    def test_create_returns_error_from_invalid_match_size(self):
        game_id = self.NUM_GAMES + 1
        create_url = '/games'
        name = get_incremental_game_name(game_id)
        description = get_incremental_game_description(game_id)
        match_size = '2.5'
        game_data = {
            'name': name,
            'description': description,
            'match_size': match_size
        }
        response = self.post(create_url, data=game_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('match_size'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(name, errors.get('inputs').get('name'))
        self.assertEqual(description, errors.get('inputs').get('description'))
        self.assertEqual(None, errors.get('inputs').get('match_size'))

    def test_create_returns_error_from_negative_match_size(self):
        game_id = self.NUM_GAMES + 1
        create_url = '/games'
        name = get_incremental_game_name(game_id)
        description = get_incremental_game_description(game_id)
        match_size = -1
        game_data = {
            'name': name,
            'description': description,
            'match_size': match_size
        }
        response = self.post(create_url, data=game_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('match_size'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(name, errors.get('inputs').get('name'))
        self.assertEqual(description, errors.get('inputs').get('description'))
        self.assertEqual(match_size, errors.get('inputs').get('match_size'))

    def test_create_returns_created_status(self):
        game_id = self.NUM_GAMES + 1
        create_url = '/games'
        name = get_incremental_game_name(game_id)
        description = get_incremental_game_description(game_id)
        game_data = {
            'name': name,
            'description': description,
            'match_size': 2
        }
        response = self.post(create_url, data=game_data)
        self.assertEqual(201, response.status_code)
        game = json.loads(response.data)
        self.assertIsNotNone(game.get('id'))
        self.assertIsNotNone(game.get('date_created'))
        self.assertIsNotNone(game.get('date_modified'))
        self.assertEqual(name, game.get('name'))
        self.assertEqual(description, game.get('description'))
        self.assertEqual(2, game.get('match_size'))
        self.assertEqual(True, game.get('is_active'))

        # Make sure the game was actually saved to the database
        saved_game = GamesService.get_instance().get(int(game.get('id')))
        self.assertEqual(saved_game.get_id(), game.get('id'))
        self.assertEqual(Game.dump_datetime(saved_game.get_date_created()), game.get('date_created'))
        self.assertEqual(Game.dump_datetime(saved_game.get_date_modified()), game.get('date_modified'))
        self.assertEqual(saved_game.get_name(), game.get('name'))
        self.assertEqual(saved_game.get_description(), game.get('description'))
        self.assertEqual(saved_game.get_match_size(), game.get('match_size'))
        self.assertEqual(saved_game.get_is_active(), game.get('is_active'))


class GamesShow(NoAuthTest):

    def test_show_errors_for_nonexistent_game(self):
        game_id = self.NUM_GAMES + 1
        show_url = '/games/{}'.format(game_id)
        response = self.get(show_url)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('GameNotFound'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(game_id, errors.get('inputs').get('id'))

    def test_show_returns_game(self):
        show_url = '/games/{}'.format(self.game.get_id())
        response = self.get(show_url)
        self.assertEqual(200, response.status_code)
        game = json.loads(response.data)
        self.assertEqual(self.game.get_id(), game.get('id'))
        self.assertIsNotNone(game.get('date_created'))
        self.assertIsNotNone(game.get('date_modified'))
        self.assertEqual(self.game.get_name(), game.get('name'))
        self.assertEqual(self.game.get_description(), game.get('description'))
        self.assertEqual(self.game.get_match_size(), game.get('match_size'))
        self.assertEqual(self.game.get_is_active(), game.get('is_active'))


class GamesUpdate(NoAuthTest):

    def test_update_errors_for_nonexistent_game(self):
        game_id = self.NUM_GAMES + 1
        update_url = '/games/{}'.format(game_id)
        name = get_incremental_game_name(game_id)
        game_data = {
            'name': name
        }
        response = self.put(update_url, data=game_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('GameNotFound'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(game_id, errors.get('inputs').get('id'))

    def test_update_returns_error_from_long_name(self):
        game_id = self.game.get_id()
        update_url = '/games/{}'.format(game_id)
        name = 'x' * (Game.NAME_MAX_LENGTH + 1)
        game_data = {
            'name': name
        }
        response = self.put(update_url, data=game_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('name'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(game_id, errors.get('inputs').get('id'))
        self.assertEqual(name, errors.get('inputs').get('name'))
        self.assertEqual('', errors.get('inputs').get('description'))
        self.assertEqual(False, errors.get('inputs').get('is_active'))

    def test_update_returns_error_from_name_not_unique(self):
        game_id = self.game.get_id()
        game_number = 1 if game_id == 2 else 2
        update_url = '/games/{}'.format(game_id)
        name = get_incremental_game_name(game_number)
        game_data = {
            'name': name,
        }
        response = self.put(update_url, data=game_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('IntegrityError'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(game_id, errors.get('inputs').get('id'))
        self.assertEqual(name, errors.get('inputs').get('name'))
        self.assertEqual('', errors.get('inputs').get('description'))
        self.assertEqual(False, errors.get('inputs').get('is_active'))

    def test_update_returns_error_from_long_description(self):
        game_id = self.game.get_id()
        update_url = '/games/{}'.format(game_id)
        description = 'x' * (Game.DESCRIPTION_MAX_LENGTH + 1)
        game_data = {
            'description': description
        }
        response = self.put(update_url, data=game_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('description'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(game_id, errors.get('inputs').get('id'))
        self.assertEqual('', errors.get('inputs').get('name'))
        self.assertEqual(description, errors.get('inputs').get('description'))
        self.assertEqual(False, errors.get('inputs').get('is_active'))

    def test_update_returns_error_from_illegal_update_to_match_size(self):
        update_url = '/games/{}'.format(self.game.get_id())
        match_size = '2.5'
        game_data = {
            'match_size': match_size
        }
        response = self.put(update_url, data=game_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('AttributeError'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual('', errors.get('inputs').get('name'))
        self.assertEqual('', errors.get('inputs').get('description'))
        self.assertEqual(False, errors.get('inputs').get('is_active'))
        self.assertEqual(None, errors.get('inputs').get('match_size'))

    def test_update_updates_game(self):
        update_url = '/games/{}'.format(self.game.get_id())
        game_number = self.game.get_id() * 100
        name = get_incremental_game_name(game_number)
        description = get_incremental_game_description(game_number)
        match_size = self.game.get_match_size()
        game_data = {
            'name': name,
            'description': description,
            'is_active': False
        }
        response = self.put(update_url, data=game_data)
        self.assertEqual(200, response.status_code)
        game = json.loads(response.data)
        self.assertIsNotNone(game.get('id'))
        self.assertIsNotNone(game.get('date_created'))
        self.assertIsNotNone(game.get('date_modified'))
        self.assertEqual(name, game.get('name'))
        self.assertEqual(description, game.get('description'))
        self.assertEqual(match_size, game.get('match_size'))
        self.assertEqual(False, game.get('is_active'))

        # Make sure the game was actually updated in the database
        saved_game = GamesService.get_instance().get(int(game.get('id')))
        self.assertEqual(saved_game.get_id(), game.get('id'))
        self.assertEqual(Game.dump_datetime(saved_game.get_date_created()), game.get('date_created'))
        self.assertEqual(Game.dump_datetime(saved_game.get_date_modified()), game.get('date_modified'))
        self.assertEqual(saved_game.get_name(), game.get('name'))
        self.assertEqual(saved_game.get_description(), game.get('description'))
        self.assertEqual(saved_game.get_match_size(), game.get('match_size'))
        self.assertEqual(saved_game.get_is_active(), game.get('is_active'))


class GamesDelete(NoAuthTest):

    def test_delete_errors_for_nonexistent_game(self):
        game_id = self.NUM_GAMES + 1
        delete_url = '/games/{}'.format(game_id)
        response = self.delete(delete_url)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('GameNotFound'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(game_id, errors.get('inputs').get('id'))

    def test_delete_deletes_game(self):
        delete_url = '/games/{}'.format(self.game.get_id())
        self.assertEqual(True, self.game.get_is_active())
        response = self.delete(delete_url)
        self.assertEqual(200, response.status_code)
        game = json.loads(response.data)
        self.assertIsNotNone(game.get('id'))
        self.assertIsNotNone(game.get('date_created'))
        self.assertIsNotNone(game.get('date_modified'))
        self.assertIsNotNone(game.get('name'))
        self.assertIsNotNone(game.get('description'))
        self.assertIsNotNone(game.get('match_size'))
        self.assertEqual(False, game.get('is_active'))

        # Make sure the game was actually updated in the database
        saved_game = GamesService.get_instance().get(int(game.get('id')))
        self.assertEqual(saved_game.get_id(), game.get('id'))
        self.assertEqual(Game.dump_datetime(saved_game.get_date_created()), game.get('date_created'))
        self.assertEqual(Game.dump_datetime(saved_game.get_date_modified()), game.get('date_modified'))
        self.assertEqual(saved_game.get_name(), game.get('name'))
        self.assertEqual(saved_game.get_description(), game.get('description'))
        self.assertEqual(saved_game.get_match_size(), game.get('match_size'))
        self.assertEqual(saved_game.get_is_active(), game.get('is_active'))


def main():
    unittest.main()

if __name__ == '__main__':
    main()