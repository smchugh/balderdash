# Import flask dependencies
from flask import Blueprint

# Import input validators
from application.inputs.Matches import ListInputs, CreateInputs

# Import models
from application.models.Match import Match

# Import services
from application.services.GamesService import GamesService
from application.services.PlayersService import PlayersService
from application.services.MatchesService import MatchesService

# Import view rendering
from application.controllers import get_inputs, render_view, authenticate, get_current_user

# Define the blueprint
matches_module = Blueprint('matches', __name__, url_prefix='/matches')

# Set some common error constants
NOT_FOUND_ERROR = {'MatchNotFound': ['Unable to find Match']}
GAME_NOT_FOUND_ERROR = {'GameNotFound': ['Unable to find the specified Game']}
OPPONENT_NOT_FOUND_ERROR = {'OpponentNotFound': ['Unable to find specified Opponent']}


# Set the route and accepted methods
@matches_module.route('', methods=['GET'])
@authenticate
def index():
    # Get the input validator
    inputs = ListInputs(get_inputs())

    # Verify the list inputs
    if inputs.validate():
        matches = MatchesService.get_instance().get_list_by_game_for_player(
            inputs.game_id.data, get_current_user().get_id(), inputs.limit.data, inputs.offset.data
        )

        return render_view('matches/index', 200, matches={match.get_id(): match.serialized for match in matches})

    return render_view('422', 422, errors=inputs.errors, inputs=inputs.serialized())


# Set the route and accepted methods
@matches_module.route('', methods=['POST'])
@authenticate
def create():
    # Get the input validator
    inputs = CreateInputs(get_inputs())

    # Verify the match creation inputs
    if inputs.validate_on_submit():
        # Ensure we have a valid game
        game = GamesService.get_instance().get(inputs.game_id.data)
        if game:
            # If an opponent is specified, match with that opponent
            if inputs.opponent_id.data:
                # Ensure that the opponent is a valid user
                opponent = PlayersService.get_instance().get(inputs.opponent_id.data)
                if not opponent:
                    return render_view('422', 422, errors=OPPONENT_NOT_FOUND_ERROR, inputs=inputs.serialized())

                # First attempt to find a match already requested by the desired opponent
                match = MatchesService.get_instance().get_opponent_match(
                    game.get_id(), get_current_user(), opponent.get_id()
                )

                # If the match is found, add the player to it and start the match if it's full
                if match:
                    match.add_player(get_current_user())

                # If no match is found, create one that is assigned to the desired opponent,
                # but leave it in the waiting state
                else:
                    match = Match(game, get_current_user())
                    match.add_player(opponent, should_start=False)

            # Otherwise, match with a random opponent
            else:
                # First, attempt to find a match that is looking for an opponent
                match = MatchesService.get_instance().get_random_match(game.get_id(), get_current_user())

                # If the match is found, add the player to it and start the match if it's full
                if match:
                    match.add_player(get_current_user())

                # If no match is found, create one that is waiting for an opponent
                else:
                    match = Match(game, get_current_user())

            try:
                match.save()
                return render_view('matches/show', 201, match=match.serialized)
            except Exception as e:
                return render_view('422', 422, errors={e.__class__.__name__: [e.message]}, inputs=inputs.serialized())

        return render_view('422', 422, errors=GAME_NOT_FOUND_ERROR, inputs=inputs.serialized())

    return render_view('422', 422, errors=inputs.errors, inputs=inputs.serialized())


# Set the route and accepted methods
@matches_module.route('/<int:match_id>', methods=['GET'])
@authenticate
def show(match_id):
    # Get the match
    match = MatchesService.get_instance().get(match_id)

    if match:
        return render_view('matches/show', 200, match=match.serialized)

    return render_view('422', 422, errors=NOT_FOUND_ERROR, inputs={'id': match.get_id()})

# Set the route and accepted methods
@matches_module.route('/<int:match_id>', methods=['PUT'])
@authenticate
def update(match_id):
    # Get the match
    match = MatchesService.get_instance().get(match_id)

    #### Then determine which turn and state - acting as validation that the inputs provided are for the right state

    # Get all turns for match_id == match_id && date_completed == NULL && date_cancelled == NULL && state IN (0, 1),
    # ordered by date_created ASC

    ### For each turn

    # Get the turn_definition_fillers for this turn

    # If player_id == player_id, this is a selector turn for this player, otherwise it's a supplier turn

    ## If selector turn

    # If count of turn_definition_fillers < game.definition_filler_count
    # :: return STATE_SUPPLYING state and an empty definitions array (end loop)

    # Elseif state == STATE_SUPPLYING || (state == STATE_SELECTING && there is not a turn_definition_filler with selector_id)
    # :: **If this is an update**
    # :: :: set the selector_id == player_id for the given turn_definition_filler
    # :: Else
    # :: :: set turn state to STATE_SELECTING, return STATE_SELECTING state and the definitions (end loop)

    # Elseif state == STATE_SELECTING && there is a turn_definition_filler with selector_id && there is no next turn
    # :: *create next turn* and add to array of turns so that we iterate to it

    # If we reach this point, we iterate to next turn

    ## Else (If supplier turn)

    # If there is a turn_definition_filler with supplier_id == player_id
    # :: If there is a turn_definition_filler with selector_id
    # :: :: If this turn_player has viewed the replay
    # :: :: :: continue
    # :: :: Return *replay*
    # :: Else
    # :: :: Return state (end loop) {{ hold player here or should we let them move to the next turn? }}

    # Else
    # :: **If this is an update**
    # :: :: create the turn_definition_filler from the inputs
    # :: Else
    # :: :: Return the definition template

    #### 'Return's mean send inputs off to turn endpoint for the right state to perform validation and proper actions
