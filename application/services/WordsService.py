import random

from application.models.Word import Word
from application.services.BaseService import BaseService
from application.services.TurnsService import TurnsService


class WordsService(BaseService):
    def __init__(self):
        super(WordsService, self).__init__(Word)

    def get_all_active_ids(self):
        return self.get_class().select(
            self.get_class()._id
        ).filter(
            self.get_class()._is_active is True
        ).all()

    def get_new_word_for_match(self, match_id):
        excluded_word_ids = TurnsService.get_instance().get_used_word_ids(match_id)
        valid_ids = self.get_all_active_ids()
        word = None

        while word is None and len(valid_ids) > 0:
            valid_ids = list(set(valid_ids) - set(excluded_word_ids))
            word_id = random.choice(valid_ids)
            word = self.get(word_id)
            excluded_word_ids = [word_id]
