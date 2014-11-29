from application.models.Game import Game
from application.services.BaseService import BaseService


class GamesService(BaseService):
    def __init__(self):
        super(GamesService, self).__init__(Game)
