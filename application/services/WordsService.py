from application.models.Word import Word
from application.services.BaseService import BaseService


class WordsService(BaseService):
    def __init__(self):
        super(WordsService, self).__init__(Word)
