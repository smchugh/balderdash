# Import flask dependencies
from flask import Blueprint

# Import input validators
from application.inputs.Matches import ListInputs, CreateInputs

# Import models
from application.models.Match import Match
from application.models.Player import Player
from application.models.Game import Game

# Define the blueprint
matches_module = Blueprint('matches', __name__, url_prefix='/matches')

# Import view rendering
from application.controllers import get_inputs, render_view, authenticate, get_current_user

# Set some common error constants
NOT_FOUND_ERROR = {'MatchNotFound': ['Unable to find Match']}
GAME_NOT_FOUND_ERROR = {'GameNotFound': ['Unable to find the specified Game']}
OPPONENT_NOT_FOUND_ERROR = {'OpponentNotFound': ['Unable to find specified Opponent']}


# Set the route and accepted methods
@matches_module.route('/', methods=['GET'])
@authenticate
def index():
    # Get the input validator
    inputs = ListInputs(get_inputs())

    # Verify the list inputs
    if inputs.validate():
        matches = Match.get_list_by_game_for_player(
            inputs.game_id.data, get_current_user().get_id(), inputs.limit.data, inputs.offset.data
        )
        print get_current_user().get_id()

        return render_view('matches/index', 200, matches={match.get_id(): match.serialized for match in matches})

    return render_view('422', 422, errors=inputs.errors, inputs=inputs.serialized())


# Set the route and accepted methods
@matches_module.route('/', methods=['POST'])
@authenticate
def create():
    # Get the input validator
    inputs = CreateInputs(get_inputs())

    # Verify the match creation inputs
    if inputs.validate_on_submit():
        # Ensure we have a valid game
        game = Game.get(inputs.game_id.data)
        if game:
            # If an opponent is specified, match with that opponent
            if inputs.opponent_id.data:
                # Ensure that the opponent is a valid user
                opponent = Player.get(inputs.opponent_id.data)
                if not opponent:
                    return render_view('422', 422, errors=OPPONENT_NOT_FOUND_ERROR, inputs=inputs.serialized())

                # First attempt to find a match already requested by the desired opponent
                match = Match.get_opponent_match(game.get_id(), get_current_user(), opponent.get_id())

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
                match = Match.get_random_match(game.get_id(), get_current_user())

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
    match = Match.get(match_id)

    if match:
        return render_view('matches/show', 200, match=match.serialized)

    return render_view('422', 422, errors=NOT_FOUND_ERROR, inputs={'id': match.get_id()})
