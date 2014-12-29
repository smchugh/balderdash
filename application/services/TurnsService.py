from application.models.Turn import Turn
from application.services.BaseService import BaseService


class TurnsService(BaseService):
    def __init__(self):
        super(TurnsService, self).__init__(Turn)

    def function(self):
        pass
