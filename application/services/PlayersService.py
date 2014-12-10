from application.models.Player import Player
from application.services.BaseService import BaseService


class PlayersService(BaseService):
    def __init__(self):
        super(PlayersService, self).__init__(Player)

    def get_from_auth(self, auth_token):
        return self.get_class().query.filter_by(_auth_token=auth_token).first()

    def get_from_username(self, username):
        return self.get_class().query.filter_by(_username=username).first()
