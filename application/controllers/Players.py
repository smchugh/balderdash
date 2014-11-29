# Import flask dependencies
from flask import Blueprint

# Import password / encryption helper tools
from werkzeug.security import check_password_hash

# Import input validators
from application.inputs.Players import ListInputs, CreateInputs, UpdateInputs, SignInInputs

# Import models
from application.models.Player import Player

# Import services
from application.services.PlayersService import PlayersService

# Import view rendering
from application.controllers import get_inputs, render_view, authenticate, \
    get_current_user, get_mixed_dict_from_multidict

# Define the blueprint
players_module = Blueprint('players', __name__, url_prefix='/players')

# Set some common error constants
NOT_FOUND_ERROR = {'PlayerNotFound': ['Unable to find Player']}
INVALID_USERNAME_PASSWORD_ERROR = {'InvalidInputs': ['Wrong username or password']}
UNABLE_TO_SIGNIN_ERROR = {'SigninError': ['Unable to sign in an inactive player']}
UNABLE_TO_SIGNOUT_ERROR = {'SignoutError': ['Unable to sign out player']}


# Set the route and accepted methods
@players_module.route('/', methods=['GET'])
def index():
    # Get the input validator
    inputs = ListInputs(get_inputs())

    # Verify the list inputs
    if inputs.validate():

        players = PlayersService.get_instance().get_list(inputs.limit.data, inputs.offset.data)

        return render_view('players/index', 200, players={player.get_id(): player.serialized for player in players})

    return render_view('422', 422, errors=inputs.errors, inputs=inputs.obfuscated())


# Set the route and accepted methods
@players_module.route('/', methods=['POST'])
def create():
    # Get the input validator
    inputs = CreateInputs(get_inputs())

    # Verify the player creation inputs
    if inputs.validate_on_submit():

        avatar_url = inputs.avatar_url.data if inputs.avatar_url.data else None
        player = Player(inputs.username.data, inputs.password.data, inputs.email.data, avatar_url)
        try:
            player.save()
            player_data = dict(player.serialized.items() + {'auth_token': player.get_auth_token()}.items())
            return render_view('players/show', 201, player=player_data)
        except Exception as e:
            return render_view('422', 422, errors={e.__class__.__name__: [e.message]}, inputs=inputs.obfuscated())

    return render_view('422', 422, errors=inputs.errors, inputs=inputs.obfuscated())


# Set the route and accepted methods
@players_module.route('/<int:player_id>', methods=['GET'])
@authenticate
def show(player_id):
    # Get the player
    player = PlayersService.get_instance().get(player_id)

    if player:
        return render_view('players/show', 200, player=player.serialized)

    return render_view('422', 422, errors=NOT_FOUND_ERROR, inputs={'id': player_id})


# Set the route and accepted methods
@players_module.route('/<int:player_id>', methods=['PUT'])
@authenticate
def update(player_id):
    # Get the player
    player = PlayersService.get_instance().get(player_id)

    # Verify the player creation inputs
    if player:

        # Get the input validator
        inputs = UpdateInputs(get_inputs())
        combined_inputs = dict(inputs.obfuscated().items() + {'id': player_id}.items())

        if inputs.validate_on_submit():

            try:
                player.update(**get_mixed_dict_from_multidict(get_inputs(), inputs))
                return render_view('players/show', 200, player=player.serialized)
            except Exception as e:
                return render_view('422', 422, errors={e.__class__.__name__: [e.message]}, inputs=combined_inputs)

        return render_view('422', 422, errors=inputs.errors, inputs=combined_inputs)

    return render_view('422', 422, errors=NOT_FOUND_ERROR, inputs={'id': player_id})


# Set the route and accepted methods
@players_module.route('/<int:player_id>', methods=['DELETE'])
@authenticate
def delete(player_id):
    # Get the player
    player = PlayersService.get_instance().get(player_id)

    # Verify the player creation inputs
    if player:
        try:
            player.update(**{'is_active': False})
            return render_view('players/show', 200, player=player.serialized)
        except Exception as e:
            return render_view('422', 422, errors={e.__class__.__name__: [e.message]}, inputs={'id': player_id})

    return render_view('422', 422, errors=NOT_FOUND_ERROR, inputs={'id': player_id})


# Set the route and accepted methods
@players_module.route('/signin/', methods=['POST'])
def signin():
    # Get the input validator
    inputs = SignInInputs(get_inputs())

    # Verify the sign in inputs
    if inputs.validate_on_submit():

        player = PlayersService.get_instance().get_from_username(inputs.username.data)

        if player and check_password_hash(player.get_password(), inputs.password.data):

            if player.login():
                player_data = dict(player.serialized.items() + {'auth_token': player.get_auth_token()}.items())
                return render_view('players/show', 200, player=player_data)
            else:
                return render_view('422', 422, errors=UNABLE_TO_SIGNIN_ERROR, inputs=inputs.obfuscated())

        return render_view('422', 422, errors=INVALID_USERNAME_PASSWORD_ERROR, inputs=inputs.obfuscated())

    return render_view('422', 422, errors=inputs.errors, inputs=inputs.obfuscated())


# Set the route and accepted methods
@players_module.route('/signout/', methods=['POST'])
@authenticate
def signout():
    if get_current_user() and get_current_user().logout():
        return render_view('players/show', 200, player={'Success': 'Player signed out'})
    else:
        return render_view('422', 422, errors=UNABLE_TO_SIGNOUT_ERROR)
