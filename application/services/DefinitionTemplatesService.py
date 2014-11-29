from application.models.DefinitionTemplate import DefinitionTemplate
from application.services.BaseService import BaseService


class DefinitionTemplatesService(BaseService):
    def __init__(self):
        super(DefinitionTemplatesService, self).__init__(DefinitionTemplate)

    def get_list_by_word(self, word_id, limit, offset):
        return self.get_list_query(limit, offset).filter(
            self.get_class()._word_id == word_id
        ).all()