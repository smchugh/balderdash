# Import flask dependencies
from flask import Blueprint

# Import input validators
from application.inputs.Games import ListInputs, CreateInputs, UpdateInputs

# Import models
from application.models.Game import Game

# Import services
from application.services.GamesService import GamesService

# Import view rendering
from application.controllers import get_inputs, render_view, get_mixed_dict_from_multidict

# Define the blueprint
games_module = Blueprint('games', __name__, url_prefix='/games')

# Set some common error constants
NOT_FOUND_ERROR = {'GameNotFound': ['Unable to find Game']}


# Set the route and accepted methods
@games_module.route('/', methods=['GET'])
def index():
    # Get the input validator
    inputs = ListInputs(get_inputs())

    # Verify the list inputs
    if inputs.validate():

        games = GamesService.get_instance().get_list(inputs.limit.data, inputs.offset.data)

        return render_view('games/index', 200, games={game.get_id(): game.serialized for game in games})

    return render_view('422', 422, errors=inputs.errors, inputs=inputs.serialized())


# Set the route and accepted methods
@games_module.route('/', methods=['POST'])
def create():
    # Get the input validator
    inputs = CreateInputs(get_inputs())

    # Verify the game creation inputs
    if inputs.validate_on_submit():

        game = Game(inputs.name.data, inputs.description.data, inputs.match_size.data)
        try:
            game.save()
            return render_view('games/show', 201, game=game.serialized)
        except Exception as e:
            return render_view('422', 422, errors={e.__class__.__name__: [e.message]}, inputs=inputs.serialized())

    return render_view('422', 422, errors=inputs.errors, inputs=inputs.serialized())


# Set the route and accepted methods
@games_module.route('/<int:game_id>', methods=['GET'])
def show(game_id):
    # Get the game
    game = GamesService.get_instance().get(game_id)

    if game:
        return render_view('games/show', 200, game=game.serialized)

    return render_view('422', 422, errors=NOT_FOUND_ERROR, inputs={'id': game_id})


# Set the route and accepted methods
@games_module.route('/<int:game_id>', methods=['PUT'])
def update(game_id):
    # Get the game
    game = GamesService.get_instance().get(game_id)

    # Verify the game creation inputs
    if game:

        # Get the input validator
        inputs = UpdateInputs(get_inputs())
        combined_inputs = dict(inputs.serialized().items() + {'id': game_id}.items())

        if inputs.validate_on_submit():

            try:
                game.update(**get_mixed_dict_from_multidict(get_inputs(), inputs))
                return render_view('games/show', 200, game=game.serialized)
            except Exception as e:
                return render_view('422', 422, errors={e.__class__.__name__: [e.message]}, inputs=combined_inputs)

        return render_view('422', 422, errors=inputs.errors, inputs=combined_inputs)

    return render_view('422', 422, errors=NOT_FOUND_ERROR, inputs={'id': game_id})


# Set the route and accepted methods
@games_module.route('/<int:game_id>', methods=['DELETE'])
def delete(game_id):
    # Get the game
    game = GamesService.get_instance().get(game_id)

    # Verify the game creation inputs
    if game:
        try:
            game.update(**{'is_active': False})
            return render_view('games/show', 200, game=game.serialized)
        except Exception as e:
            return render_view('422', 422, errors={e.__class__.__name__: [e.message]}, inputs={'id': game_id})

    return render_view('422', 422, errors=NOT_FOUND_ERROR, inputs={'id': game_id})
