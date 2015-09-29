from application.models.Turn import Turn
from application.models.TurnPlayer import TurnPlayer
from application.services.BaseService import BaseService
from application.services.MatchesService import MatchesService
from application.services.PlayersService import PlayersService
from application.services.WordsService import WordsService
from application.services.TurnDefinitionFillersService import TurnDefinitionFillersService
from application.services.TurnPlayersService import TurnPlayersService
from application.controllers.Matches import NOT_FOUND_ERROR, TURN_NOT_FOUND_ERROR


class TurnsService(BaseService):
    def __init__(self):
        super(TurnsService, self).__init__(Turn)

    # Get all turns for match_id && date_completed == NULL && date_cancelled == NULL && state IN (0, 1),
    # ordered by date_created ASC
    def get_active_turns(self, match_id):
        return self.get_class().query.filter(
            self.get_class()._match_id == match_id,
            self.get_class()._date_completed == None,
            self.get_class()._date_canceled == None,
            self.get_class()._state in [Turn.STATE_SUPPLYING[0], Turn.STATE_SELECTING[0]]
        ).order_by(
            self.get_class()._date_created.asc()
        ).all()

    def get_used_word_ids(self, match_id):
        return self.get_class().select(
            self.get_class().word_id
        ).filter(
            self.get_class()._match_id == match_id
        ).all()

    def get_last_selector_id_for_match(self, match_id):
        self.get_class().select(TurnPlayer._player_id).join(
            TurnPlayer
        ).filter(
            self.get_class()._match_id == match_id,
            TurnPlayer._is_selector is True,
            self.get_class()._sate != Turn.STATE_CANCELED[0]
        ).order_by(
            self.get_class()._date_created().desc()
        ).first()

    def create_new_turn(self, match):
        # TODO Add logic to determine if we should create a new turn or end the game

        # Determine word for this turn
        word = WordsService.get_instance().get_new_word_for_match(match.get_id())

        # Determine selector for this turn
        selector = PlayersService.get_instance().get_next_selector_for_match(match)

        # Save the new turn
        return self.get_class()(match, selector, word).save()

    def get_player_turn(self, match_id, player_id):
        # Get the match
        match = MatchesService.get_instance().get_for_player(match_id, player_id)

        if not match:
            return None, NOT_FOUND_ERROR

        turns = self.get_active_turns(match_id)

        if not turns:
            turns = [self.create_new_turn(match)]

        for i, turn in enumerate(turns):
            turn_definition_fillers = TurnDefinitionFillersService.get_instance().get_list_by_turn(turn.get_id())

            turn_player = TurnPlayersService.get_instance().get_for_turn_by_player(turn.get_id(), player_id)

            # If this player is the selector for this turn
            if turn_player.get_is_selector():
                # If the turn is in the supplying state, or the turn is in the selecting state, but this selector
                # has not yet made a selection, then this is the current turn for this player
                if turn.get_state() == Turn.STATE_SUPPLYING[0] or \
                        (
                            turn.get_state() == Turn.STATE_SELECTING[0] and
                            all(
                                turn_definition_filler.get_selector_id() is None
                                for turn_definition_filler in turn_definition_fillers
                            )
                        ):
                    return turn, None

                # If this is not the current turn for this player, and there exists no next turn, create one
                elif i + 1 == len(turns):
                    turns = [self.create_new_turn(match)]

            # Otherwise, if:
            #  - this player is a supplier for this turn, and
            #  -- this player still needs to supply a definition for this turn, or
            #  -- this player has already supplied a definition for this turn but the selector has not made a selection
            elif all(
                not turn_definition_filler.get_supplier_id() == player_id
                for turn_definition_filler in turn_definition_fillers
            ) or any(
                turn_definition_filler.get_selector_id() is not None
                for turn_definition_filler in turn_definition_fillers
            ):
                return turn, None

        return None, TURN_NOT_FOUND_ERROR
