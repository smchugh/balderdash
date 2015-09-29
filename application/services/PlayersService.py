from application.models.Player import Player
from application.services.BaseService import BaseService
from application.services.TurnsService import TurnsService


class PlayersService(BaseService):
    def __init__(self):
        super(PlayersService, self).__init__(Player)

    def get_from_auth(self, auth_token):
        return self.get_class().query.filter_by(_auth_token=auth_token).first()

    def get_from_username(self, username):
        return self.get_class().query.filter_by(_username=username).first()

    def get_next_selector_for_match(self, match):
        # Get players in order
        player_ids = [player.get_id() for player in match.get_players()]

        # Get the last selector
        last_selector_id = TurnsService.get_instance().get_last_selector_id_for_match(match.get_id())
        last_selector_index = player_ids.index(last_selector_id)

        if not last_selector_index:
            return None

        # Get the next selector in order
        return self.get(
            player_ids[(last_selector_index + 1) % len(player_ids)]
        )