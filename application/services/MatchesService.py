from application.models.Match import Match, match_players
from application.models.Game import Game
from application.services.BaseService import BaseService
from application.services.TurnsService import TurnsService
from application.services.PlayersService import PlayersService


class MatchesService(BaseService):
    def __init__(self):
        super(MatchesService, self).__init__(Match)

    def get_list_by_game_for_player(self, game_id, player_id, limit, offset):
        return self.get_class().query.join(
            match_players
        ).filter(
            match_players.c.player_id == player_id,
            self.get_class()._game_id == game_id
        ).order_by(self.get_class()._id).limit(limit).offset(offset).all()

    def get_opponent_match(self, game_id, player, opponent_id):
        # TODO return only the matches for this game with null start and cancel dates as a subquery before joining

        return self.get_class().query.join(
            match_players
        ).filter(
            self.get_class()._game_id == game_id,
            self.get_class()._date_started == None,
            self.get_class()._date_canceled == None,
            match_players.c.player_id == opponent_id,
            # TODO replace with sqlalchemy subquery
            '{} NOT IN (SELECT player_id FROM match_players WHERE match_players.match_id = matches._id)'.format(
                player.get_id()
            )
        ).order_by(
            self.get_class()._date_created.asc()
        ).with_for_update().first()

    def get_random_match(self, game_id, player):
        return self.get_class().query.join(
            match_players, Game
        ).filter(
            self.get_class()._game_id == game_id,
            self.get_class()._date_started == None,
            self.get_class()._date_canceled == None,
            # TODO replace with sqlalchemy subquery
            '{} NOT IN (SELECT player_id FROM match_players WHERE match_players.match_id = matches._id)'.format(
                player.get_id()
            ),
            # TODO replace with sqlalchemy subquery
            'games._match_size > (SELECT COUNT(*) FROM match_players WHERE match_players.match_id = matches._id)'
        ).order_by(
            self.get_class()._date_created.asc()
        ).with_for_update().first()

    def get_for_player(self, match_id, player_id):
        return self.get_class().query.join(
            match_players
        ).filter(
            self.get_class()._id == match_id,
            match_players.c.player_id == player_id
        ).first()
