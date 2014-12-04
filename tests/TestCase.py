import os
import unittest

from application import db
from application.models.Word import Word
from application.models.DefinitionTemplate import DefinitionTemplate
from application.models.DefinitionFiller import DefinitionFiller


WORDS = [
    {
        'lexeme_form': 'capricious',
        'lexical_class': 'adjective',
        'definition_templates': [
            {
                'definition': 'tending to make {} and {} {}',
                'filler_lexical_classes': ['adjective', 'adjective', 'noun'],
                'definition_fillers': [
                    {
                        'filler': ['sudden', 'unpredictable', 'changes'],
                        'is_dictionary': True
                    }
                ]
            },
            {
                'definition': 'in the process of {}, being {}, or starting to {}',
                'filler_lexical_classes': ['verb', 'verb', 'verb'],
                'definition_fillers': [
                    {
                        'filler': ['emerging', 'born', 'develop'],
                        'is_dictionary': False
                    },
                    {
                        'filler': ['walking', 'carried', 'crawl'],
                        'is_dictionary': False
                    },
                    {
                        'filler': ['drinking', 'drunk', 'befuddle'],
                        'is_dictionary': False
                    }
                ]
            }
        ]
    },
    {
        'lexeme_form': 'bombastic',
        'lexical_class': 'adjective',
        'definition_templates': [
            {
                'definition': 'marked by or given to {} in {} excessively lofty {}',
                'filler_lexical_classes': ['verb', 'adjective', 'noun'],
                'definition_fillers': [
                    {
                        'filler': ['speaking', 'obnoxious', 'language'],
                        'is_dictionary': True
                    },
                    {
                        'filler': ['dancing', 'beautiful', 'acrobatics'],
                        'is_dictionary': False
                    }
                ]
            },
            {
                'definition': 'extreme {} or {} marked especially by a belligerent {} policy',
                'filler_lexical_classes': ['noun', 'noun', 'adjective'],
                'definition_fillers': [
                    {
                        'filler': ['chauvinism', 'nationalism', 'foreign'],
                        'is_dictionary': False
                    },
                    {
                        'filler': ['love', 'lust', 'budgetary'],
                        'is_dictionary': False
                    }
                ]
            }
        ]
    }
]


class TestCase(unittest.TestCase):

    def run(self, result=None):
        # Abort the test suite on the first failure
        # Taken from http://stackoverflow.com/questions/685424/pyunit-stop-after-first-failing-test
        if result.failures or result.errors:
            self.tearDown()
            print 'aborted'
        else:
            super(TestCase, self).run(result)

    def setUp(self):
        # for now lets assert we never run test suite in production
        environment = os.environ.get('APPLICATION_ENV', 'testing')
        self.assertEqual(environment, 'testing')

        db.create_all()
        self.insert_dummy_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def insert_dummy_data(self):
        for word_data in WORDS:
            word = Word(word_data.get('lexeme_form'), word_data.get('lexical_class'))
            word.save()
            for template_data in word_data.get('definition_templates', []):
                template = DefinitionTemplate(
                    word, template_data.get('definition'), template_data.get('filler_lexical_classes')
                )
                template.save()
                for filler_data in template_data.get('definition_fillers', []):
                    DefinitionFiller(template, filler_data.get('filler'), filler_data.get('is_dictionary')).save()
