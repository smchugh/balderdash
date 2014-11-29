from application.models.DefinitionFiller import DefinitionFiller
from application.models.DefinitionTemplate import DefinitionTemplate
from application.services.BaseService import BaseService


class DefinitionFillersService(BaseService):
    def __init__(self):
        super(DefinitionFillersService, self).__init__(DefinitionFiller)

    def get_list_by_word(self, word_id, limit, offset):
        return self.get_list_query(limit, offset).join(
            DefinitionTemplate
        ).filter(
            DefinitionTemplate._word_id == word_id
        ).all()

    def get_list_by_definition_template(self, definition_template_id, limit, offset):
        return self.get_list_query(limit, offset).join(
            DefinitionTemplate
        ).filter(
            DefinitionTemplate._id == definition_template_id
        ).all()