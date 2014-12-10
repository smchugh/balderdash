from application.models.DefinitionTemplate import DefinitionTemplate
from application.services.BaseService import BaseService


class DefinitionTemplatesService(BaseService):
    def __init__(self):
        super(DefinitionTemplatesService, self).__init__(DefinitionTemplate)

    def get_list_by_word(self, word_id, limit=None, offset=None):
        return self.get_class().query.filter(
            self.get_class()._word_id == word_id
        ).order_by(self.get_class()._id).limit(limit).offset(offset).all()
