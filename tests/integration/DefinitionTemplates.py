import unittest
import json

from common import NoAuthTest
from application.models.DefinitionTemplate import DefinitionTemplate
from application.services.DefinitionTemplatesService import DefinitionTemplatesService


class DefinitionTemplatesIndex(NoAuthTest):

    def test_index_returns_all_definition_templates(self):
        index_url = '/definition_templates'
        response = self.get(index_url)
        self.assertEqual(200, response.status_code)
        definition_templates = json.loads(response.data)
        self.assertEqual(self.NUM_DEFINITION_TEMPLATES, len(definition_templates))

    def test_index_returns_limited_definition_templates(self):
        index_url = '/definition_templates'
        limit = int(self.NUM_DEFINITION_TEMPLATES / 2)
        query_string = {'limit': limit}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(200, response.status_code)
        definition_templates = json.loads(response.data)
        self.assertTrue(len(definition_templates) > 0)
        self.assertEqual(limit, len(definition_templates))

    def test_index_returns_offset_definition_templates(self):
        index_url = '/definition_templates'
        offset = int(self.NUM_DEFINITION_TEMPLATES / 2)
        query_string = {'offset': offset}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(200, response.status_code)
        definition_templates = json.loads(response.data)
        self.assertEqual(self.NUM_DEFINITION_TEMPLATES - offset, len(definition_templates))

    def test_index_returns_error_from_invalid_limit(self):
        index_url = '/definition_templates'
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
        index_url = '/definition_templates'
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
        index_url = '/definition_templates'
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
        index_url = '/definition_templates'
        offset = -1
        query_string = {'offset': offset}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('offset'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(offset, errors.get('inputs').get('offset'))

    def test_index_returns_definition_templates_for_word(self):
        index_url = '/definition_templates'
        word_id = self.word.get_id()
        query_string = {'word_id': word_id}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(200, response.status_code)
        definition_templates = json.loads(response.data)
        definition_templates_from_db = DefinitionTemplatesService.get_instance().get_list_by_word(word_id)
        all_definition_templates = DefinitionTemplatesService.get_instance().get_list()
        self.assertTrue(len(definition_templates) > 0)
        self.assertTrue(len(definition_templates) < len(all_definition_templates))
        self.assertEqual(len(definition_templates_from_db), len(definition_templates))

    def test_index_returns_definition_templates_for_zero_word_id(self):
        index_url = '/definition_templates'
        word_id = 0
        query_string = {'word_id': word_id}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('word_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(word_id, errors.get('inputs').get('word_id'))

    def test_index_returns_definition_templates_for_negative_word_id(self):
        index_url = '/definition_templates'
        word_id = -1
        query_string = {'word_id': word_id}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('word_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(word_id, errors.get('inputs').get('word_id'))

    def test_index_returns_definition_templates_for_invalid_word_id(self):
        index_url = '/definition_templates'
        word_id = '2.5'
        query_string = {'word_id': word_id}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('word_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(None, errors.get('inputs').get('word_id'))

    def test_index_returns_limited_definition_templates_for_word(self):
        index_url = '/definition_templates'
        word_id = self.word.get_id()
        definition_templates_from_db = DefinitionTemplatesService.get_instance().get_list_by_word(word_id)
        limit = int(len(definition_templates_from_db) / 2)
        query_string = {'word_id': word_id, 'limit': limit}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(200, response.status_code)
        definition_templates = json.loads(response.data)
        self.assertTrue(len(definition_templates) > 0)
        self.assertEqual(limit, len(definition_templates))

    def test_index_returns_offset_definition_templates_for_word(self):
        index_url = '/definition_templates'
        word_id = self.word.get_id()
        definition_templates_from_db = DefinitionTemplatesService.get_instance().get_list_by_word(word_id)
        offset = int(len(definition_templates_from_db) / 2)
        query_string = {'word_id': word_id, 'offset': offset}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(200, response.status_code)
        definition_templates = json.loads(response.data)
        self.assertEqual(len(definition_templates_from_db) - offset, len(definition_templates))


class DefinitionTemplatesCreate(NoAuthTest):

    def test_create_returns_error_from_missing_word_id(self):
        create_url = '/definition_templates'
        definition = self.definition_template.get_definition()
        filler_lexical_classes = self.definition_template.get_filler_lexical_classes()
        definition_template_data = {
            'definition': definition,
            'filler_lexical_classes': filler_lexical_classes
        }
        response = self.post(create_url, data=definition_template_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('word_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(None, errors.get('inputs').get('word_id'))
        self.assertEqual(definition, errors.get('inputs').get('definition'))
        self.assertEqual(filler_lexical_classes, errors.get('inputs').get('filler_lexical_classes'))

    def test_create_returns_error_from_zero_word_id(self):
        create_url = '/definition_templates'
        word_id = 0
        definition = self.definition_template.get_definition()
        filler_lexical_classes = self.definition_template.get_filler_lexical_classes()
        definition_template_data = {
            'word_id': word_id,
            'definition': definition,
            'filler_lexical_classes': filler_lexical_classes
        }
        response = self.post(create_url, data=definition_template_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('word_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(word_id, errors.get('inputs').get('word_id'))
        self.assertEqual(definition, errors.get('inputs').get('definition'))
        self.assertEqual(filler_lexical_classes, errors.get('inputs').get('filler_lexical_classes'))

    def test_create_returns_error_from_negative_word_id(self):
        create_url = '/definition_templates'
        word_id = -1
        definition = self.definition_template.get_definition()
        filler_lexical_classes = self.definition_template.get_filler_lexical_classes()
        definition_template_data = {
            'word_id': word_id,
            'definition': definition,
            'filler_lexical_classes': filler_lexical_classes
        }
        response = self.post(create_url, data=definition_template_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('word_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(word_id, errors.get('inputs').get('word_id'))
        self.assertEqual(definition, errors.get('inputs').get('definition'))
        self.assertEqual(filler_lexical_classes, errors.get('inputs').get('filler_lexical_classes'))

    def test_create_returns_error_from_invalid_word_id(self):
        create_url = '/definition_templates'
        word_id = '2.5'
        definition = self.definition_template.get_definition()
        filler_lexical_classes = self.definition_template.get_filler_lexical_classes()
        definition_template_data = {
            'word_id': word_id,
            'definition': definition,
            'filler_lexical_classes': filler_lexical_classes
        }
        response = self.post(create_url, data=definition_template_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('word_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(None, errors.get('inputs').get('word_id'))
        self.assertEqual(definition, errors.get('inputs').get('definition'))
        self.assertEqual(filler_lexical_classes, errors.get('inputs').get('filler_lexical_classes'))

    def test_create_returns_error_from_nonexistent_word(self):
        create_url = '/definition_templates'
        word_id = 100000
        definition = self.definition_template.get_definition()
        filler_lexical_classes = self.definition_template.get_filler_lexical_classes()
        definition_template_data = {
            'word_id': word_id,
            'definition': definition,
            'filler_lexical_classes': filler_lexical_classes
        }
        response = self.post(create_url, data=definition_template_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('WordNotFound'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(word_id, errors.get('inputs').get('word_id'))
        self.assertEqual(definition, errors.get('inputs').get('definition'))
        self.assertEqual(filler_lexical_classes, errors.get('inputs').get('filler_lexical_classes'))

    def test_create_returns_error_from_missing_definition(self):
        create_url = '/definition_templates'
        word_id = self.definition_template.get_word().get_id()
        filler_lexical_classes = self.definition_template.get_filler_lexical_classes()
        definition_template_data = {
            'word_id': word_id,
            'filler_lexical_classes': filler_lexical_classes
        }
        response = self.post(create_url, data=definition_template_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('definition'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(word_id, errors.get('inputs').get('word_id'))
        self.assertEqual('', errors.get('inputs').get('definition'))
        self.assertEqual(filler_lexical_classes, errors.get('inputs').get('filler_lexical_classes'))

    def test_create_returns_error_from_long_definition(self):
        create_url = '/definition_templates'
        word_id = self.definition_template.get_word().get_id()
        definition = 'x' * (DefinitionTemplate.DEFINITION_MAX_LENGTH + 1)
        filler_lexical_classes = self.definition_template.get_filler_lexical_classes()
        definition_template_data = {
            'word_id': word_id,
            'definition': definition,
            'filler_lexical_classes': filler_lexical_classes
        }
        response = self.post(create_url, data=definition_template_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('definition'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(word_id, errors.get('inputs').get('word_id'))
        self.assertEqual(definition, errors.get('inputs').get('definition'))
        self.assertEqual(filler_lexical_classes, errors.get('inputs').get('filler_lexical_classes'))

    def test_create_returns_error_from_missing_filler_lexical_classes(self):
        create_url = '/definition_templates'
        word_id = self.definition_template.get_word().get_id()
        definition = self.definition_template.get_definition()
        definition_template_data = {
            'word_id': word_id,
            'definition': definition
        }
        response = self.post(create_url, data=definition_template_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('filler_lexical_classes'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(word_id, errors.get('inputs').get('word_id'))
        self.assertEqual(definition, errors.get('inputs').get('definition'))
        self.assertEqual([], errors.get('inputs').get('filler_lexical_classes'))

    def test_create_returns_error_from_empty_filler_lexical_classes(self):
        create_url = '/definition_templates'
        word_id = self.definition_template.get_word().get_id()
        definition = self.definition_template.get_definition()
        filler_lexical_classes = []
        definition_template_data = {
            'word_id': word_id,
            'definition': definition,
            'filler_lexical_classes': filler_lexical_classes
        }
        response = self.post(create_url, data=definition_template_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('filler_lexical_classes'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(word_id, errors.get('inputs').get('word_id'))
        self.assertEqual(definition, errors.get('inputs').get('definition'))
        self.assertEqual(filler_lexical_classes, errors.get('inputs').get('filler_lexical_classes'))

    def test_create_returns_error_from_non_list_filler_lexical_classes(self):
        create_url = '/definition_templates'
        word_id = self.definition_template.get_word().get_id()
        definition = self.definition_template.get_definition()
        filler_lexical_classes = '123'
        definition_template_data = {
            'word_id': word_id,
            'definition': definition,
            'filler_lexical_classes': filler_lexical_classes
        }
        response = self.post(create_url, data=definition_template_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('filler_lexical_classes'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(word_id, errors.get('inputs').get('word_id'))
        self.assertEqual(definition, errors.get('inputs').get('definition'))
        self.assertEqual([filler_lexical_classes], errors.get('inputs').get('filler_lexical_classes'))

    def test_create_returns_error_from_filler_lexical_classes_with_too_many_entries(self):
        create_url = '/definition_templates'
        word_id = self.definition_template.get_word().get_id()
        definition = self.definition_template.get_definition()
        filler_lexical_classes = self.definition_template.get_filler_lexical_classes()
        filler_lexical_classes.append('noun')
        definition_template_data = {
            'word_id': word_id,
            'definition': definition,
            'filler_lexical_classes': filler_lexical_classes
        }
        response = self.post(create_url, data=definition_template_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('AttributeError'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(word_id, errors.get('inputs').get('word_id'))
        self.assertEqual(definition, errors.get('inputs').get('definition'))
        self.assertEqual(filler_lexical_classes, errors.get('inputs').get('filler_lexical_classes'))

    def test_create_returns_error_from_filler_lexical_classes_with_entry_not_a_lexical_class(self):
        create_url = '/definition_templates'
        word_id = self.definition_template.get_word().get_id()
        definition = self.definition_template.get_definition()
        filler_lexical_classes = self.definition_template.get_filler_lexical_classes()
        filler_lexical_classes[0] = 'foo'
        definition_template_data = {
            'word_id': word_id,
            'definition': definition,
            'filler_lexical_classes': filler_lexical_classes
        }
        response = self.post(create_url, data=definition_template_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('filler_lexical_classes'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(word_id, errors.get('inputs').get('word_id'))
        self.assertEqual(definition, errors.get('inputs').get('definition'))
        self.assertEqual(filler_lexical_classes, errors.get('inputs').get('filler_lexical_classes'))

    def test_create_returns_created_status(self):
        create_url = '/definition_templates'
        word = self.definition_template.get_word()
        word_id = word.get_id()
        definition = self.definition_template.get_definition()
        filler_lexical_classes = self.definition_template.get_filler_lexical_classes()
        definition_template_data = {
            'word_id': word_id,
            'definition': definition,
            'filler_lexical_classes': filler_lexical_classes
        }
        response = self.post(create_url, data=definition_template_data)
        self.assertEqual(201, response.status_code)
        definition_template = json.loads(response.data)
        self.assertIsNotNone(definition_template.get('id'))
        self.assertIsNotNone(definition_template.get('date_created'))
        self.assertIsNotNone(definition_template.get('date_modified'))
        self.assertEqual(word.serialized, definition_template.get('word'))
        self.assertEqual(definition, definition_template.get('definition'))
        self.assertEqual(filler_lexical_classes, definition_template.get('filler_lexical_classes'))
        self.assertEqual(True, definition_template.get('is_active'))

        # Make sure the definition_template was actually saved to the database
        saved_definition_template = DefinitionTemplatesService.get_instance().get(int(definition_template.get('id')))
        self.assertEqual(saved_definition_template.get_id(), definition_template.get('id'))
        self.assertEqual(DefinitionTemplate.dump_datetime(saved_definition_template.get_date_created()), definition_template.get('date_created'))
        self.assertEqual(DefinitionTemplate.dump_datetime(saved_definition_template.get_date_modified()), definition_template.get('date_modified'))
        self.assertEqual(saved_definition_template.get_word().get_id(), definition_template.get('word').get('id'))
        self.assertEqual(saved_definition_template.get_definition(), definition_template.get('definition'))
        self.assertEqual(saved_definition_template.get_filler_lexical_classes(), definition_template.get('filler_lexical_classes'))
        self.assertEqual(saved_definition_template.get_is_active(), definition_template.get('is_active'))


class DefinitionTemplatesShow(NoAuthTest):

    def test_show_errors_for_nonexistent_definition_template(self):
        definition_template_id = self.NUM_DEFINITION_TEMPLATES + 1
        show_url = '/definition_templates/{}'.format(definition_template_id)
        response = self.get(show_url)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('DefinitionTemplateNotFound'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(definition_template_id, errors.get('inputs').get('id'))

    def test_show_returns_definition_template(self):
        show_url = '/definition_templates/{}'.format(self.definition_template.get_id())
        response = self.get(show_url)
        self.assertEqual(200, response.status_code)
        definition_template = json.loads(response.data)
        self.assertEqual(self.definition_template.get_id(), definition_template.get('id'))
        self.assertIsNotNone(definition_template.get('date_created'))
        self.assertIsNotNone(definition_template.get('date_modified'))
        self.assertEqual(self.definition_template.get_word().get_id(), definition_template.get('word').get('id'))
        self.assertEqual(self.definition_template.get_definition(), definition_template.get('definition'))
        self.assertEqual(self.definition_template.get_filler_lexical_classes(), definition_template.get('filler_lexical_classes'))
        self.assertEqual(self.definition_template.get_is_active(), definition_template.get('is_active'))


class DefinitionTemplatesUpdate(NoAuthTest):

    def test_update_errors_for_nonexistent_definition_template(self):
        definition_template_id = self.NUM_DEFINITION_TEMPLATES + 1
        update_url = '/definition_templates/{}'.format(definition_template_id)
        is_active = False
        definition_template_data = {
            'is_active': is_active
        }
        response = self.put(update_url, data=definition_template_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('DefinitionTemplateNotFound'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(definition_template_id, errors.get('inputs').get('id'))

    def test_update_returns_error_from_zero_word_id(self):
        update_url = '/definition_templates/{}'.format(self.definition_template.get_id())
        word_id = 0
        definition = self.definition_template.get_definition()
        filler_lexical_classes = self.definition_template.get_filler_lexical_classes()
        definition_template_data = {
            'word_id': word_id,
            'definition': definition,
            'filler_lexical_classes': filler_lexical_classes
        }
        response = self.put(update_url, data=definition_template_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('word_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(word_id, errors.get('inputs').get('word_id'))
        self.assertEqual(definition, errors.get('inputs').get('definition'))
        self.assertEqual(filler_lexical_classes, errors.get('inputs').get('filler_lexical_classes'))

    def test_update_returns_error_from_negative_word_id(self):
        update_url = '/definition_templates/{}'.format(self.definition_template.get_id())
        word_id = -1
        definition = self.definition_template.get_definition()
        filler_lexical_classes = self.definition_template.get_filler_lexical_classes()
        definition_template_data = {
            'word_id': word_id,
            'definition': definition,
            'filler_lexical_classes': filler_lexical_classes
        }
        response = self.put(update_url, data=definition_template_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('word_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(word_id, errors.get('inputs').get('word_id'))
        self.assertEqual(definition, errors.get('inputs').get('definition'))
        self.assertEqual(filler_lexical_classes, errors.get('inputs').get('filler_lexical_classes'))

    def test_update_returns_error_from_invalid_word_id(self):
        update_url = '/definition_templates/{}'.format(self.definition_template.get_id())
        word_id = '2.5'
        definition = self.definition_template.get_definition()
        filler_lexical_classes = self.definition_template.get_filler_lexical_classes()
        definition_template_data = {
            'word_id': word_id,
            'definition': definition,
            'filler_lexical_classes': filler_lexical_classes
        }
        response = self.put(update_url, data=definition_template_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('word_id'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(None, errors.get('inputs').get('word_id'))
        self.assertEqual(definition, errors.get('inputs').get('definition'))
        self.assertEqual(filler_lexical_classes, errors.get('inputs').get('filler_lexical_classes'))

    def test_update_returns_error_from_nonexistent_word(self):
        update_url = '/definition_templates/{}'.format(self.definition_template.get_id())
        word_id = 100000
        definition = self.definition_template.get_definition()
        filler_lexical_classes = self.definition_template.get_filler_lexical_classes()
        definition_template_data = {
            'word_id': word_id,
            'definition': definition,
            'filler_lexical_classes': filler_lexical_classes
        }
        response = self.put(update_url, data=definition_template_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('WordNotFound'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(word_id, errors.get('inputs').get('word_id'))
        self.assertEqual(definition, errors.get('inputs').get('definition'))
        self.assertEqual(filler_lexical_classes, errors.get('inputs').get('filler_lexical_classes'))

    def test_update_updates_is_active_for_definition_template(self):
        update_url = '/definition_templates/{}'.format(self.definition_template.get_id())
        is_active = False
        definition_template_data = {
            'is_active': is_active
        }
        response = self.put(update_url, data=definition_template_data)
        self.assertEqual(200, response.status_code)
        definition_template = json.loads(response.data)
        self.assertIsNotNone(definition_template.get('id'))
        self.assertIsNotNone(definition_template.get('date_created'))
        self.assertIsNotNone(definition_template.get('date_modified'))
        self.assertEqual(is_active, definition_template.get('is_active'))

        # Make sure the definition_template was actually updated in the database
        saved_definition_template = DefinitionTemplatesService.get_instance().get(int(definition_template.get('id')))
        self.assertEqual(saved_definition_template.get_id(), definition_template.get('id'))
        self.assertEqual(DefinitionTemplate.dump_datetime(saved_definition_template.get_date_created()), definition_template.get('date_created'))
        self.assertEqual(DefinitionTemplate.dump_datetime(saved_definition_template.get_date_modified()), definition_template.get('date_modified'))
        self.assertEqual(saved_definition_template.get_word().get_id(), definition_template.get('word').get('id'))
        self.assertEqual(saved_definition_template.get_definition(), definition_template.get('definition'))
        self.assertEqual(saved_definition_template.get_filler_lexical_classes(), definition_template.get('filler_lexical_classes'))
        self.assertEqual(saved_definition_template.get_is_active(), definition_template.get('is_active'))

    def test_update_creates_definition_template_and_inactivates_existing_definition_template(self):
        definition_template_id = self.definition_template.get_id()
        update_url = '/definition_templates/{}'.format(definition_template_id)
        self.assertEqual(True, self.definition_template.get_is_active())
        word_id = self.definition_template.get_word().get_id()
        definition = self.definition_template.get_definition()
        filler_lexical_classes = self.definition_template.get_filler_lexical_classes()
        definition_template_data = {
            'word_id': word_id,
            'definition': definition
        }
        response = self.put(update_url, data=definition_template_data)
        self.assertEqual(200, response.status_code)
        definition_template = json.loads(response.data)
        self.assertIsNotNone(definition_template.get('id'))
        self.assertIsNotNone(definition_template.get('date_created'))
        self.assertIsNotNone(definition_template.get('date_modified'))
        self.assertEqual(word_id, definition_template.get('word').get('id'))
        self.assertEqual(definition, definition_template.get('definition'))
        self.assertEqual(filler_lexical_classes, definition_template.get('filler_lexical_classes'))
        self.assertNotEqual(definition_template_id, definition_template.get('id'))
        self.assertIsNotNone(definition_template.get('is_active'))

        # Make sure the definition_template was actually updated in the database
        saved_definition_template = DefinitionTemplatesService.get_instance().get(int(definition_template.get('id')))
        self.assertEqual(saved_definition_template.get_id(), definition_template.get('id'))
        self.assertEqual(DefinitionTemplate.dump_datetime(saved_definition_template.get_date_created()), definition_template.get('date_created'))
        self.assertEqual(DefinitionTemplate.dump_datetime(saved_definition_template.get_date_modified()), definition_template.get('date_modified'))
        self.assertEqual(saved_definition_template.get_word().get_id(), definition_template.get('word').get('id'))
        self.assertEqual(saved_definition_template.get_definition(), definition_template.get('definition'))
        self.assertEqual(saved_definition_template.get_filler_lexical_classes(), definition_template.get('filler_lexical_classes'))
        self.assertEqual(saved_definition_template.get_is_active(), definition_template.get('is_active'))

        # Ensure old definition template was marked inactive
        old_definition_template = DefinitionTemplatesService.get_instance().get(definition_template_id)
        self.assertEqual(False, old_definition_template.get_is_active())


class DefinitionTemplatesDelete(NoAuthTest):

    def test_delete_errors_for_nonexistent_definition_template(self):
        definition_template_id = self.NUM_DEFINITION_TEMPLATES + 1
        delete_url = '/definition_templates/{}'.format(definition_template_id)
        response = self.delete(delete_url)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('DefinitionTemplateNotFound'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(definition_template_id, errors.get('inputs').get('id'))

    def test_delete_deletes_definition_template(self):
        delete_url = '/definition_templates/{}'.format(self.definition_template.get_id())
        self.assertEqual(True, self.definition_template.get_is_active())
        response = self.delete(delete_url)
        self.assertEqual(200, response.status_code)
        definition_template = json.loads(response.data)
        self.assertIsNotNone(definition_template.get('id'))
        self.assertIsNotNone(definition_template.get('date_created'))
        self.assertIsNotNone(definition_template.get('date_modified'))
        self.assertIsNotNone(definition_template.get('word'))
        self.assertIsNotNone(definition_template.get('definition'))
        self.assertIsNotNone(definition_template.get('filler_lexical_classes'))
        self.assertEqual(False, definition_template.get('is_active'))

        # Make sure the definition_template was actually updated in the database
        saved_definition_template = DefinitionTemplatesService.get_instance().get(int(definition_template.get('id')))
        self.assertEqual(saved_definition_template.get_id(), definition_template.get('id'))
        self.assertEqual(DefinitionTemplate.dump_datetime(saved_definition_template.get_date_created()), definition_template.get('date_created'))
        self.assertEqual(DefinitionTemplate.dump_datetime(saved_definition_template.get_date_modified()), definition_template.get('date_modified'))
        self.assertEqual(saved_definition_template.get_word().get_id(), definition_template.get('word').get('id'))
        self.assertEqual(saved_definition_template.get_definition(), definition_template.get('definition'))
        self.assertEqual(saved_definition_template.get_filler_lexical_classes(), definition_template.get('filler_lexical_classes'))
        self.assertEqual(saved_definition_template.get_is_active(), definition_template.get('is_active'))


def main():
    unittest.main()

if __name__ == '__main__':
    main()