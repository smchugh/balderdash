import unittest
import json

from common import NoAuthTest
from application.models.Word import Word
from application.services.WordsService import WordsService


class WordsIndex(NoAuthTest):

    def test_index_returns_all_words(self):
        index_url = '/words'
        response = self.get(index_url)
        self.assertEqual(200, response.status_code)
        words = json.loads(response.data)
        self.assertEqual(self.NUM_WORDS, len(words))

    def test_index_returns_limited_words(self):
        index_url = '/words'
        limit = int(self.NUM_WORDS / 2)
        query_string = {'limit': limit}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(200, response.status_code)
        words = json.loads(response.data)
        self.assertTrue(len(words) > 0)
        self.assertEqual(limit, len(words))

    def test_index_returns_offset_words(self):
        index_url = '/words'
        offset = int(self.NUM_WORDS / 2)
        query_string = {'offset': offset}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(200, response.status_code)
        words = json.loads(response.data)
        self.assertEqual(self.NUM_WORDS - offset, len(words))

    def test_index_returns_error_from_invalid_limit(self):
        index_url = '/words'
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
        index_url = '/words'
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
        index_url = '/words'
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
        index_url = '/words'
        offset = -1
        query_string = {'offset': offset}
        response = self.get(index_url, query_string=query_string)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('offset'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(offset, errors.get('inputs').get('offset'))


class WordsCreate(NoAuthTest):

    def test_create_returns_error_from_missing_lexeme_form(self):
        create_url = '/words'
        lexical_class = self.word.get_lexical_class()
        word_data = {
            'lexical_class': lexical_class
        }
        response = self.post(create_url, data=word_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('lexeme_form'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual('', errors.get('inputs').get('lexeme_form'))
        self.assertEqual(lexical_class, errors.get('inputs').get('lexical_class'))

    def test_create_returns_error_from_long_lexeme_form(self):
        create_url = '/words'
        lexeme_form = 'x' * (Word.LEXEME_FORM_MAX_LENGTH + 1)
        lexical_class = self.word.get_lexical_class()
        word_data = {
            'lexeme_form': lexeme_form,
            'lexical_class': lexical_class
        }
        response = self.post(create_url, data=word_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('lexeme_form'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(lexeme_form, errors.get('inputs').get('lexeme_form'))
        self.assertEqual(lexical_class, errors.get('inputs').get('lexical_class'))

    def test_create_returns_error_from_missing_lexical_class(self):
        create_url = '/words'
        lexeme_form = 'foo'
        word_data = {
            'lexeme_form': lexeme_form
        }
        response = self.post(create_url, data=word_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('lexical_class'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(lexeme_form, errors.get('inputs').get('lexeme_form'))
        self.assertEqual('', errors.get('inputs').get('lexical_class'))

    def test_create_returns_error_from_lexical_class_not_a_valid_lexical_class(self):
        create_url = '/words'
        lexeme_form = 'foo'
        lexical_class = 'bar'
        word_data = {
            'lexeme_form': lexeme_form,
            'lexical_class': lexical_class
        }
        response = self.post(create_url, data=word_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('lexical_class'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(lexeme_form, errors.get('inputs').get('lexeme_form'))
        self.assertEqual(lexical_class, errors.get('inputs').get('lexical_class'))

    def test_create_returns_created_status(self):
        create_url = '/words'
        lexeme_form = 'foo'
        lexical_class = Word.LEXICAL_CLASSES[0]
        word_data = {
            'lexeme_form': lexeme_form,
            'lexical_class': lexical_class
        }
        response = self.post(create_url, data=word_data)
        self.assertEqual(201, response.status_code)
        word = json.loads(response.data)
        self.assertIsNotNone(word.get('id'))
        self.assertIsNotNone(word.get('date_created'))
        self.assertIsNotNone(word.get('date_modified'))
        self.assertEqual(lexeme_form, word.get('lexeme_form'))
        self.assertEqual(lexical_class, word.get('lexical_class'))
        self.assertEqual(True, word.get('is_active'))

        # Make sure the word was actually saved to the database
        saved_word = WordsService.get_instance().get(int(word.get('id')))
        self.assertEqual(saved_word.get_id(), word.get('id'))
        self.assertEqual(Word.dump_datetime(saved_word.get_date_created()), word.get('date_created'))
        self.assertEqual(Word.dump_datetime(saved_word.get_date_modified()), word.get('date_modified'))
        self.assertEqual(saved_word.get_lexeme_form(), word.get('lexeme_form'))
        self.assertEqual(saved_word.get_lexical_class(), word.get('lexical_class'))
        self.assertEqual(saved_word.get_is_active(), word.get('is_active'))


class WordsShow(NoAuthTest):

    def test_show_errors_for_nonexistent_word(self):
        word_id = self.NUM_WORDS + 1
        show_url = '/words/{}'.format(word_id)
        response = self.get(show_url)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('WordNotFound'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(word_id, errors.get('inputs').get('id'))

    def test_show_returns_word(self):
        show_url = '/words/{}'.format(self.word.get_id())
        response = self.get(show_url)
        self.assertEqual(200, response.status_code)
        word = json.loads(response.data)
        self.assertEqual(self.word.get_id(), word.get('id'))
        self.assertIsNotNone(word.get('date_created'))
        self.assertIsNotNone(word.get('date_modified'))
        self.assertEqual(self.word.get_lexeme_form(), word.get('lexeme_form'))
        self.assertEqual(self.word.get_lexical_class(), word.get('lexical_class'))
        self.assertEqual(self.word.get_is_active(), word.get('is_active'))


class WordsUpdate(NoAuthTest):

    def test_update_errors_for_nonexistent_word(self):
        word_id = self.NUM_WORDS + 1
        update_url = '/words/{}'.format(word_id)
        is_active = False
        word_data = {
            'is_active': is_active
        }
        response = self.put(update_url, data=word_data)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('WordNotFound'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(word_id, errors.get('inputs').get('id'))

    def test_update_updates_is_active_for_word(self):
        update_url = '/words/{}'.format(self.word.get_id())
        is_active = False
        word_data = {
            'is_active': is_active
        }
        response = self.put(update_url, data=word_data)
        self.assertEqual(200, response.status_code)
        word = json.loads(response.data)
        self.assertIsNotNone(word.get('id'))
        self.assertIsNotNone(word.get('date_created'))
        self.assertIsNotNone(word.get('date_modified'))
        self.assertEqual(is_active, word.get('is_active'))

        # Make sure the word was actually updated in the database
        saved_word = WordsService.get_instance().get(int(word.get('id')))
        self.assertEqual(saved_word.get_id(), word.get('id'))
        self.assertEqual(Word.dump_datetime(saved_word.get_date_created()), word.get('date_created'))
        self.assertEqual(Word.dump_datetime(saved_word.get_date_modified()), word.get('date_modified'))
        self.assertEqual(saved_word.get_lexeme_form(), word.get('lexeme_form'))
        self.assertEqual(saved_word.get_lexical_class(), word.get('lexical_class'))
        self.assertEqual(saved_word.get_is_active(), word.get('is_active'))

    def test_update_creates_word_and_inactivates_existing_word(self):
        word_id = self.word.get_id()
        update_url = '/words/{}'.format(word_id)
        self.assertEqual(True, self.word.get_is_active())
        lexeme_form = self.word.get_lexeme_form()
        lexical_class = Word.LEXICAL_CLASSES[0]
        word_data = {
            'lexeme_form': lexeme_form,
            'lexical_class': lexical_class
        }
        response = self.put(update_url, data=word_data)
        self.assertEqual(200, response.status_code)
        word = json.loads(response.data)
        self.assertIsNotNone(word.get('id'))
        self.assertIsNotNone(word.get('date_created'))
        self.assertIsNotNone(word.get('date_modified'))
        self.assertEqual(lexeme_form, word.get('lexeme_form'))
        self.assertEqual(lexical_class, word.get('lexical_class'))
        self.assertNotEqual(word_id, word.get('id'))
        self.assertIsNotNone(word.get('is_active'))

        # Make sure the word was actually updated in the database
        saved_word = WordsService.get_instance().get(int(word.get('id')))
        self.assertEqual(saved_word.get_id(), word.get('id'))
        self.assertEqual(Word.dump_datetime(saved_word.get_date_created()), word.get('date_created'))
        self.assertEqual(Word.dump_datetime(saved_word.get_date_modified()), word.get('date_modified'))
        self.assertEqual(saved_word.get_lexeme_form(), word.get('lexeme_form'))
        self.assertEqual(saved_word.get_lexical_class(), word.get('lexical_class'))
        self.assertEqual(saved_word.get_is_active(), word.get('is_active'))

        # Ensure old lexeme_form template was marked inactive
        old_word = WordsService.get_instance().get(word_id)
        self.assertEqual(False, old_word.get_is_active())


class WordsDelete(NoAuthTest):

    def test_delete_errors_for_nonexistent_word(self):
        word_id = self.NUM_WORDS + 1
        delete_url = '/words/{}'.format(word_id)
        response = self.delete(delete_url)
        self.assertEqual(422, response.status_code)
        errors = json.loads(response.data)
        self.assertIsNotNone(errors.get('errors'))
        self.assertIsNotNone(errors.get('errors').get('WordNotFound'))
        self.assertIsNotNone(errors.get('inputs'))
        self.assertEqual(word_id, errors.get('inputs').get('id'))

    def test_delete_deletes_word(self):
        delete_url = '/words/{}'.format(self.word.get_id())
        self.assertEqual(True, self.word.get_is_active())
        response = self.delete(delete_url)
        self.assertEqual(200, response.status_code)
        word = json.loads(response.data)
        self.assertIsNotNone(word.get('id'))
        self.assertIsNotNone(word.get('date_created'))
        self.assertIsNotNone(word.get('date_modified'))
        self.assertIsNotNone(word.get('lexeme_form'))
        self.assertIsNotNone(word.get('lexical_class'))
        self.assertEqual(False, word.get('is_active'))

        # Make sure the word was actually updated in the database
        saved_word = WordsService.get_instance().get(int(word.get('id')))
        self.assertEqual(saved_word.get_id(), word.get('id'))
        self.assertEqual(Word.dump_datetime(saved_word.get_date_created()), word.get('date_created'))
        self.assertEqual(Word.dump_datetime(saved_word.get_date_modified()), word.get('date_modified'))
        self.assertEqual(saved_word.get_lexeme_form(), word.get('lexeme_form'))
        self.assertEqual(saved_word.get_lexical_class(), word.get('lexical_class'))
        self.assertEqual(saved_word.get_is_active(), word.get('is_active'))


def main():
    unittest.main()

if __name__ == '__main__':
    main()