from application.models.TurnDefinitionFiller import TurnDefinitionFiller
from application.services.BaseService import BaseService


class TurnDefinitionFillersService(BaseService):
    def __init__(self):
        super(TurnDefinitionFillersService, self).__init__(TurnDefinitionFiller)

    def get_list_by_turn(self, turn_id):
        return self.get_class().query.filter(
            self.get_class()._turn_id == turn_id
        ).all()
