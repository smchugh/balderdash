import unittest
import json

from common import NoAuthTest
from application.models.DefinitionFiller import DefinitionFiller
from application.services.DefinitionFillersService import DefinitionFillersService


class DefinitionFillersIndex(NoAuthTest):

    def test_index_returns_all_definition_fillers(self):
        index_url = '/definition_fillers'
        response = self.get(index_url)
        self.assertEqual(200, response.status_code)
        definition_fillers = json.loads(response.data)
        self.assertEqual(self.NUM_DEFINITION_FILLERS, len(definition_fillers))

    def test_index_returns_limited_definition_fillers(self):
        index_url = '/definition_fillers'
        limit = int(self.NUM_DEFINITION_FILLERS / 2)
        query_string = {'limit': limit}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(200, response.status_code)
        definition_fillers = json.loads(response.data)
        self.assertTrue(len(definition_fillers) > 0)
        self.assertEqual(limit, len(definition_fillers))

    def test_index_returns_offset_definition_fillers(self):
        index_url = '/definition_fillers'
        offset = int(self.NUM_DEFINITION_FILLERS / 2)
        query_string = {'offset': offset}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(200, response.status_code)
        definition_fillers = json.loads(response.data)
        self.assertEqual(self.NUM_DEFINITION_FILLERS - offset, len(definition_fillers))

    def test_index_returns_error_from_invalid_limit(self):
        index_url = '/definition_fillers'
        limit = '2.5'
        query_string = {'limit': limit}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('limit'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(None, errors.get('inputs').get('limit'))

    def test_index_returns_error_from_negative_limit(self):
        index_url = '/definition_fillers'
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
        index_url = '/definition_fillers'
        offset = '2.5'
        query_string = {'offset': offset}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('offset'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(None, errors.get('inputs').get('offset'))

    def test_index_returns_error_from_negative_offset(self):
        index_url = '/definition_fillers'
        offset = -1
        query_string = {'offset': offset}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('offset'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(offset, errors.get('inputs').get('offset'))

    def test_index_returns_definition_fillers_for_word(self):
        index_url = '/definition_fillers'
        word_id = self.word.get_id()
        query_string = {'word_id': word_id}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(200, response.status_code)
        definition_fillers = json.loads(response.data)
        definition_fillers_from_db = DefinitionFillersService.get_instance().get_list_by_word(word_id)
        all_definition_fillers = DefinitionFillersService.get_instance().get_list()
        self.assertTrue(len(definition_fillers) > 0)
        self.assertTrue(len(definition_fillers) < len(all_definition_fillers))
        self.assertEqual(len(definition_fillers_from_db), len(definition_fillers))

    def test_index_returns_definition_fillers_for_zero_word_id(self):
        index_url = '/definition_fillers'
        word_id = 0
        query_string = {'word_id': word_id}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('word_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(word_id, errors.get('inputs').get('word_id'))

    def test_index_returns_definition_fillers_for_negative_word_id(self):
        index_url = '/definition_fillers'
        word_id = -1
        query_string = {'word_id': word_id}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('word_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(word_id, errors.get('inputs').get('word_id'))

    def test_index_returns_definition_fillers_for_invalid_word_id(self):
        index_url = '/definition_fillers'
        word_id = '2.5'
        query_string = {'word_id': word_id}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('word_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(None, errors.get('inputs').get('word_id'))

    def test_index_returns_limited_definition_fillers_for_word(self):
        index_url = '/definition_fillers'
        word_id = self.word.get_id()
        definition_fillers_from_db = DefinitionFillersService.get_instance().get_list_by_word(word_id)
        limit = int(len(definition_fillers_from_db) / 2)
        query_string = {'word_id': word_id, 'limit': limit}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(200, response.status_code)
        definition_fillers = json.loads(response.data)
        self.assertTrue(len(definition_fillers) > 0)
        self.assertEqual(limit, len(definition_fillers))

    def test_index_returns_offset_definition_fillers_for_word(self):
        index_url = '/definition_fillers'
        word_id = self.word.get_id()
        definition_fillers_from_db = DefinitionFillersService.get_instance().get_list_by_word(word_id)
        offset = int(len(definition_fillers_from_db) / 2)
        query_string = {'word_id': word_id, 'offset': offset}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(200, response.status_code)
        definition_fillers = json.loads(response.data)
        self.assertEqual(len(definition_fillers_from_db) - offset, len(definition_fillers))

    def test_index_returns_definition_fillers_for_definition_template(self):
        index_url = '/definition_fillers'
        definition_template_id = self.definition_template.get_id()
        query_string = {'definition_template_id': definition_template_id}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(200, response.status_code)
        definition_fillers = json.loads(response.data)
        definition_fillers_from_db = DefinitionFillersService.get_instance().get_list_by_definition_template(definition_template_id)
        all_definition_fillers = DefinitionFillersService.get_instance().get_list()
        self.assertTrue(len(definition_fillers) > 0)
        self.assertTrue(len(definition_fillers) < len(all_definition_fillers))
        self.assertEqual(len(definition_fillers_from_db), len(definition_fillers))

    def test_index_returns_definition_fillers_for_zero_definition_template_id(self):
        index_url = '/definition_fillers'
        definition_template_id = 0
        query_string = {'definition_template_id': definition_template_id}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('definition_template_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(definition_template_id, errors.get('inputs').get('definition_template_id'))

    def test_index_returns_definition_fillers_for_negative_definition_template_id(self):
        index_url = '/definition_fillers'
        definition_template_id = -1
        query_string = {'definition_template_id': definition_template_id}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('definition_template_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(definition_template_id, errors.get('inputs').get('definition_template_id'))

    def test_index_returns_definition_fillers_for_invalid_definition_template_id(self):
        index_url = '/definition_fillers'
        definition_template_id = '2.5'
        query_string = {'definition_template_id': definition_template_id}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('definition_template_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(None, errors.get('inputs').get('definition_template_id'))

    def test_index_returns_limited_definition_fillers_for_definition_template(self):
        index_url = '/definition_fillers'
        definition_template_id = self.definition_template.get_id()
        definition_fillers_from_db = DefinitionFillersService.get_instance().get_list_by_definition_template(definition_template_id)
        limit = int(len(definition_fillers_from_db) / 2)
        query_string = {'definition_template_id': definition_template_id, 'limit': limit}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(200, response.status_code)
        definition_fillers = json.loads(response.data)
        self.assertTrue(len(definition_fillers) > 0)
        self.assertEqual(limit, len(definition_fillers))

    def test_index_returns_offset_definition_fillers_for_definition_template(self):
        index_url = '/definition_fillers'
        definition_template_id = self.definition_template.get_id()
        definition_fillers_from_db = DefinitionFillersService.get_instance().get_list_by_definition_template(definition_template_id)
        offset = int(len(definition_fillers_from_db) / 2)
        query_string = {'definition_template_id': definition_template_id, 'offset': offset}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(200, response.status_code)
        definition_fillers = json.loads(response.data)
        self.assertEqual(len(definition_fillers_from_db) - offset, len(definition_fillers))


class DefinitionFillersCreate(NoAuthTest):

    def test_create_returns_error_from_missing_definition_template_id(self):
        create_url = '/definition_fillers'
        filler = self.definition_filler.get_filler()
        definition_filler_data = {
            'filler': filler
        }
        response = self.post(create_url, data=definition_filler_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('definition_template_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(None, errors.get('inputs').get('definition_template_id'))
        self.assertEqual(filler, errors.get('inputs').get('filler'))
        self.assertEqual(False, errors.get('inputs').get('is_dictionary'))

    def test_create_returns_error_from_zero_definition_template_id(self):
        create_url = '/definition_fillers'
        definition_template_id = 0
        filler = self.definition_filler.get_filler()
        definition_filler_data = {
            'definition_template_id': definition_template_id,
            'filler': filler
        }
        response = self.post(create_url, data=definition_filler_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('definition_template_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(definition_template_id, errors.get('inputs').get('definition_template_id'))
        self.assertEqual(filler, errors.get('inputs').get('filler'))
        self.assertEqual(False, errors.get('inputs').get('is_dictionary'))

    def test_create_returns_error_from_negative_definition_template_id(self):
        create_url = '/definition_fillers'
        definition_template_id = -1
        filler = self.definition_filler.get_filler()
        definition_filler_data = {
            'definition_template_id': definition_template_id,
            'filler': filler
        }
        response = self.post(create_url, data=definition_filler_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('definition_template_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(definition_template_id, errors.get('inputs').get('definition_template_id'))
        self.assertEqual(filler, errors.get('inputs').get('filler'))
        self.assertEqual(False, errors.get('inputs').get('is_dictionary'))

    def test_create_returns_error_from_invalid_definition_template_id(self):
        create_url = '/definition_fillers'
        definition_template_id = '2.5'
        filler = self.definition_filler.get_filler()
        definition_filler_data = {
            'definition_template_id': definition_template_id,
            'filler': filler
        }
        response = self.post(create_url, data=definition_filler_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('definition_template_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(None, errors.get('inputs').get('definition_template_id'))
        self.assertEqual(filler, errors.get('inputs').get('filler'))
        self.assertEqual(False, errors.get('inputs').get('is_dictionary'))

    def test_create_returns_error_from_nonexistent_definition_template(self):
        create_url = '/definition_fillers'
        definition_template_id = 100000
        filler = self.definition_filler.get_filler()
        definition_filler_data = {
            'definition_template_id': definition_template_id,
            'filler': filler
        }
        response = self.post(create_url, data=definition_filler_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('DefinitionTemplateNotFound'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(definition_template_id, errors.get('inputs').get('definition_template_id'))
        self.assertEqual(filler, errors.get('inputs').get('filler'))
        self.assertEqual(False, errors.get('inputs').get('is_dictionary'))

    def test_create_returns_error_from_missing_filler(self):
        create_url = '/definition_fillers'
        definition_template_id = self.definition_filler.get_definition_template().get_id()
        definition_filler_data = {
            'definition_template_id': definition_template_id
        }
        response = self.post(create_url, data=definition_filler_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('filler'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(definition_template_id, errors.get('inputs').get('definition_template_id'))
        self.assertEqual([], errors.get('inputs').get('filler'))
        self.assertEqual(False, errors.get('inputs').get('is_dictionary'))

    def test_create_returns_error_from_empty_filler(self):
        create_url = '/definition_fillers'
        definition_template_id = self.definition_filler.get_definition_template().get_id()
        filler = []
        definition_filler_data = {
            'definition_template_id': definition_template_id,
            'filler': filler
        }
        response = self.post(create_url, data=definition_filler_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('filler'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(definition_template_id, errors.get('inputs').get('definition_template_id'))
        self.assertEqual(filler, errors.get('inputs').get('filler'))
        self.assertEqual(False, errors.get('inputs').get('is_dictionary'))

    def test_create_returns_error_for_invalid_filler(self):
        create_url = '/definition_fillers'
        definition_template_id = self.definition_filler.get_definition_template().get_id()
        filler = '123'
        definition_filler_data = {
            'definition_template_id': definition_template_id,
            'filler': filler
        }
        response = self.post(create_url, data=definition_filler_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('AttributeError'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(definition_template_id, errors.get('inputs').get('definition_template_id'))
        self.assertEqual([filler], errors.get('inputs').get('filler'))
        self.assertEqual(False, errors.get('inputs').get('is_dictionary'))

    def test_create_returns_error_from_filler_with_too_many_entries(self):
        create_url = '/definition_fillers'
        definition_template_id = self.definition_filler.get_definition_template().get_id()
        filler = self.definition_filler.get_filler()
        filler.append('foo')
        definition_filler_data = {
            'definition_template_id': definition_template_id,
            'filler': filler
        }
        response = self.post(create_url, data=definition_filler_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('AttributeError'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(definition_template_id, errors.get('inputs').get('definition_template_id'))
        self.assertEqual(filler, errors.get('inputs').get('filler'))
        self.assertEqual(False, errors.get('inputs').get('is_dictionary'))

    def test_create_returns_created_status(self):
        create_url = '/definition_fillers'
        definition_template = self.definition_filler.get_definition_template()
        definition_template_id = definition_template.get_id()
        filler = self.definition_filler.get_filler()
        is_dictionary = True
        definition_filler_data = {
            'definition_template_id': definition_template_id,
            'filler': filler,
            'is_dictionary': is_dictionary
        }
        response = self.post(create_url, data=definition_filler_data)
        self.assertEqual(201, response.status_code)
        definition_filler = json.loads(response.data)
        self.assertIsNotNone(definition_filler.get('id'))
        self.assertIsNotNone(definition_filler.get('date_created'))
        self.assertIsNotNone(definition_filler.get('date_modified'))
        self.assertEqual(definition_template.serialized, definition_filler.get('definition_template'))
        self.assertEqual(filler, definition_filler.get('filler'))
        self.assertEqual(is_dictionary, definition_filler.get('is_dictionary'))
        self.assertEqual(True, definition_filler.get('is_active'))

        # Make sure the definition_filler was actually saved to the database
        saved_definition_filler = DefinitionFillersService.get_instance().get(int(definition_filler.get('id')))
        self.assertEqual(saved_definition_filler.get_id(), definition_filler.get('id'))
        self.assertEqual(DefinitionFiller.dump_datetime(saved_definition_filler.get_date_created()), definition_filler.get('date_created'))
        self.assertEqual(DefinitionFiller.dump_datetime(saved_definition_filler.get_date_modified()), definition_filler.get('date_modified'))
        self.assertEqual(saved_definition_filler.get_definition_template().get_id(), definition_filler.get('definition_template').get('id'))
        self.assertEqual(saved_definition_filler.get_filler(), definition_filler.get('filler'))
        self.assertEqual(saved_definition_filler.get_is_dictionary(), definition_filler.get('is_dictionary'))
        self.assertEqual(saved_definition_filler.get_is_active(), definition_filler.get('is_active'))


class DefinitionFillersShow(NoAuthTest):

    def test_show_errors_for_nonexistent_definition_filler(self):
        definition_filler_id = self.NUM_DEFINITION_FILLERS + 1
        show_url = '/definition_fillers/{}'.format(definition_filler_id)
        response = self.get(show_url)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('DefinitionFillerNotFound'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(definition_filler_id, errors.get('inputs').get('id'))

    def test_show_returns_definition_filler(self):
        show_url = '/definition_fillers/{}'.format(self.definition_filler.get_id())
        response = self.get(show_url)
        self.assertEqual(200, response.status_code)
        definition_filler = json.loads(response.data)
        self.assertEqual(self.definition_filler.get_id(), definition_filler.get('id'))
        self.assertIsNotNone(definition_filler.get('date_created'))
        self.assertIsNotNone(definition_filler.get('date_modified'))
        self.assertEqual(self.definition_filler.get_definition_template().get_id(), definition_filler.get('definition_template').get('id'))
        self.assertEqual(self.definition_filler.get_filler(), definition_filler.get('filler'))
        self.assertEqual(self.definition_filler.get_is_dictionary(), definition_filler.get('is_dictionary'))
        self.assertEqual(self.definition_filler.get_is_active(), definition_filler.get('is_active'))


class DefinitionFillersUpdate(NoAuthTest):

    def test_update_errors_for_nonexistent_definition_filler(self):
        definition_filler_id = self.NUM_DEFINITION_FILLERS + 1
        update_url = '/definition_fillers/{}'.format(definition_filler_id)
        is_active = False
        definition_filler_data = {
            'is_active': is_active
        }
        response = self.put(update_url, data=definition_filler_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('DefinitionFillerNotFound'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(definition_filler_id, errors.get('inputs').get('id'))

    def test_update_returns_error_from_zero_definition_template_id(self):
        update_url = '/definition_fillers/{}'.format(self.definition_filler.get_id())
        definition_template_id = 0
        filler = self.definition_filler.get_filler()
        definition_filler_data = {
            'definition_template_id': definition_template_id,
            'filler': filler
        }
        response = self.put(update_url, data=definition_filler_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('definition_template_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(definition_template_id, errors.get('inputs').get('definition_template_id'))
        self.assertEqual(filler, errors.get('inputs').get('filler'))
        self.assertEqual(False, errors.get('inputs').get('is_dictionary'))

    def test_update_returns_error_from_negative_definition_template_id(self):
        update_url = '/definition_fillers/{}'.format(self.definition_filler.get_id())
        definition_template_id = -1
        filler = self.definition_filler.get_filler()
        definition_filler_data = {
            'definition_template_id': definition_template_id,
            'filler': filler
        }
        response = self.put(update_url, data=definition_filler_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('definition_template_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(definition_template_id, errors.get('inputs').get('definition_template_id'))
        self.assertEqual(filler, errors.get('inputs').get('filler'))
        self.assertEqual(False, errors.get('inputs').get('is_dictionary'))

    def test_update_returns_error_from_invalid_definition_template_id(self):
        update_url = '/definition_fillers/{}'.format(self.definition_filler.get_id())
        definition_template_id = '2.5'
        filler = self.definition_filler.get_filler()
        definition_filler_data = {
            'definition_template_id': definition_template_id,
            'filler': filler
        }
        response = self.put(update_url, data=definition_filler_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('definition_template_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(None, errors.get('inputs').get('definition_template_id'))
        self.assertEqual(filler, errors.get('inputs').get('filler'))
        self.assertEqual(False, errors.get('inputs').get('is_dictionary'))

    def test_update_returns_error_from_nonexistent_definition_template(self):
        update_url = '/definition_fillers/{}'.format(self.definition_filler.get_id())
        definition_template_id = 100000
        filler = self.definition_filler.get_filler()
        definition_filler_data = {
            'definition_template_id': definition_template_id,
            'filler': filler
        }
        response = self.put(update_url, data=definition_filler_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('DefinitionTemplateNotFound'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(definition_template_id, errors.get('inputs').get('definition_template_id'))
        self.assertEqual(filler, errors.get('inputs').get('filler'))
        self.assertEqual(False, errors.get('inputs').get('is_dictionary'))

    def test_update_updates_is_active_for_definition_filler(self):
        update_url = '/definition_fillers/{}'.format(self.definition_filler.get_id())
        is_active = False
        definition_filler_data = {
            'is_active': is_active
        }
        response = self.put(update_url, data=definition_filler_data)
        self.assertEqual(200, response.status_code)
        definition_filler = json.loads(response.data)
        self.assertIsNotNone(definition_filler.get('id'))
        self.assertIsNotNone(definition_filler.get('date_created'))
        self.assertIsNotNone(definition_filler.get('date_modified'))
        self.assertEqual(is_active, definition_filler.get('is_active'))

        # Make sure the definition_filler was actually updated in the database
        saved_definition_filler = DefinitionFillersService.get_instance().get(int(definition_filler.get('id')))
        self.assertEqual(saved_definition_filler.get_id(), definition_filler.get('id'))
        self.assertEqual(DefinitionFiller.dump_datetime(saved_definition_filler.get_date_created()), definition_filler.get('date_created'))
        self.assertEqual(DefinitionFiller.dump_datetime(saved_definition_filler.get_date_modified()), definition_filler.get('date_modified'))
        self.assertEqual(saved_definition_filler.get_definition_template().get_id(), definition_filler.get('definition_template').get('id'))
        self.assertEqual(saved_definition_filler.get_filler(), definition_filler.get('filler'))
        self.assertEqual(saved_definition_filler.get_is_dictionary(), definition_filler.get('is_dictionary'))
        self.assertEqual(saved_definition_filler.get_is_active(), definition_filler.get('is_active'))

    def test_update_creates_definition_filler_and_inactivates_existing_definition_filler(self):
        definition_filler_id = self.definition_filler.get_id()
        update_url = '/definition_fillers/{}'.format(definition_filler_id)
        self.assertEqual(True, self.definition_filler.get_is_active())
        definition_template_id = self.definition_filler.get_definition_template().get_id()
        filler = self.definition_filler.get_filler()
        definition_filler_data = {
            'definition_template_id': definition_template_id,
            'filler': filler
        }
        response = self.put(update_url, data=definition_filler_data)
        self.assertEqual(200, response.status_code)
        definition_filler = json.loads(response.data)
        self.assertIsNotNone(definition_filler.get('id'))
        self.assertIsNotNone(definition_filler.get('date_created'))
        self.assertIsNotNone(definition_filler.get('date_modified'))
        self.assertEqual(definition_template_id, definition_filler.get('definition_template').get('id'))
        self.assertEqual(filler, definition_filler.get('filler'))
        self.assertNotEqual(definition_filler_id, definition_filler.get('id'))
        self.assertIsNotNone(definition_filler.get('is_active'))

        # Make sure the definition_filler was actually updated in the database
        saved_definition_filler = DefinitionFillersService.get_instance().get(int(definition_filler.get('id')))
        self.assertEqual(saved_definition_filler.get_id(), definition_filler.get('id'))
        self.assertEqual(DefinitionFiller.dump_datetime(saved_definition_filler.get_date_created()), definition_filler.get('date_created'))
        self.assertEqual(DefinitionFiller.dump_datetime(saved_definition_filler.get_date_modified()), definition_filler.get('date_modified'))
        self.assertEqual(saved_definition_filler.get_definition_template().get_id(), definition_filler.get('definition_template').get('id'))
        self.assertEqual(saved_definition_filler.get_filler(), definition_filler.get('filler'))
        self.assertEqual(saved_definition_filler.get_is_dictionary(), definition_filler.get('is_dictionary'))
        self.assertEqual(saved_definition_filler.get_is_active(), definition_filler.get('is_active'))

        # Ensure old definition template was marked inactive
        old_definition_filler = DefinitionFillersService.get_instance().get(definition_filler_id)
        self.assertEqual(False, old_definition_filler.get_is_active())


class DefinitionFillersDelete(NoAuthTest):

    def test_delete_errors_for_nonexistent_definition_filler(self):
        definition_filler_id = self.NUM_DEFINITION_FILLERS + 1
        delete_url = '/definition_fillers/{}'.format(definition_filler_id)
        response = self.delete(delete_url)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('DefinitionFillerNotFound'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(definition_filler_id, errors.get('inputs').get('id'))

    def test_delete_deletes_definition_filler(self):
        delete_url = '/definition_fillers/{}'.format(self.definition_filler.get_id())
        self.assertEqual(True, self.definition_filler.get_is_active())
        response = self.delete(delete_url)
        self.assertEqual(200, response.status_code)
        definition_filler = json.loads(response.data)
        self.assertIsNotNone(definition_filler.get('id'))
        self.assertIsNotNone(definition_filler.get('date_created'))
        self.assertIsNotNone(definition_filler.get('date_modified'))
        self.assertIsNotNone(definition_filler.get('definition_template'))
        self.assertIsNotNone(definition_filler.get('filler'))
        self.assertIsNotNone(definition_filler.get('is_dictionary'))
        self.assertEqual(False, definition_filler.get('is_active'))

        # Make sure the definition_filler was actually updated in the database
        saved_definition_filler = DefinitionFillersService.get_instance().get(int(definition_filler.get('id')))
        self.assertEqual(saved_definition_filler.get_id(), definition_filler.get('id'))
        self.assertEqual(DefinitionFiller.dump_datetime(saved_definition_filler.get_date_created()), definition_filler.get('date_created'))
        self.assertEqual(DefinitionFiller.dump_datetime(saved_definition_filler.get_date_modified()), definition_filler.get('date_modified'))
        self.assertEqual(saved_definition_filler.get_definition_template().get_id(), definition_filler.get('definition_template').get('id'))
        self.assertEqual(saved_definition_filler.get_filler(), definition_filler.get('filler'))
        self.assertEqual(saved_definition_filler.get_is_dictionary(), definition_filler.get('is_dictionary'))
        self.assertEqual(saved_definition_filler.get_is_active(), definition_filler.get('is_active'))


def main():
    unittest.main()

if __name__ == '__main__':
    main()