from application.models.TurnPlayer import TurnPlayer
from application.services.BaseService import BaseService


class TurnPlayersService(BaseService):
    def __init__(self):
        super(TurnPlayersService, self).__init__(TurnPlayer)

    def get_for_turn_by_player(self, turn_id, player_id):
        return self.get_class().query.filter(
            self.get_class()._turn_id == turn_id,
            self.get_class()._player_id == player_id
        ).first()
