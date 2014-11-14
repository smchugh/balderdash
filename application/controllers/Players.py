# Import flask dependencies
from flask import Blueprint, request, jsonify
from flask.ext.login import login_user

# Import password / encryption helper tools
from werkzeug.security import generate_password_hash, check_password_hash

# Import input validators
from application.inputs.Players import ListInputs, CreateInputs, UpdateInputs, SignInInputs

# Import models
from application.models.Player import Player

# Define the blueprint
players_module = Blueprint('players', __name__, url_prefix='/players')

# Set some common error constants
NOT_FOUND_ERROR = {'NotFound': ['Unable to find Player']}
INVALID_USERNAME_PASSWORD_ERROR = {'InvalidInputs': ['Wrong username or password']}
UNABLE_TO_SIGNIN_ERROR = {'SigninError': ['Unable to sign in an inactive player']}


# Set the route and accepted methods
@players_module.route('/', methods=['GET'])
def index():
    # Get the input validator
    inputs = ListInputs(request.values)

    # Verify the list inputs
    if inputs.validate():

        players = Player.query.order_by(Player.id).limit(inputs.limit.data).offset(inputs.offset.data).all()

        return jsonify({player.id: player.serialized for player in players}), 200

    return jsonify({'errors': inputs.errors, 'inputs': inputs.obfuscated()}), 422


# Set the route and accepted methods
@players_module.route('/', methods=['POST'])
def create():
    # Get the input validator
    inputs = CreateInputs(request.values)

    # Verify the player creation inputs
    if inputs.validate_on_submit():

        player = Player(inputs.username.data, generate_password_hash(inputs.password.data))
        try:
            player.save()
            return jsonify(player.serialized), 201
        except Exception as e:
            return jsonify({'errors': {e.__class__.__name__: [e.message]}, 'inputs': inputs.obfuscated()}), 422

    return jsonify({'errors': inputs.errors, 'inputs': inputs.obfuscated()}), 422


# Set the route and accepted methods
@players_module.route('/<int:player_id>', methods=['GET'])
def get(player_id):
    # Get the player
    player = Player.query.filter_by(id=player_id).first()

    if player:
        return jsonify(player.serialized), 200

    return jsonify({'errors': NOT_FOUND_ERROR, 'inputs': {'id': player_id}}), 422


# Set the route and accepted methods
@players_module.route('/<int:player_id>', methods=['PUT'])
def update(player_id):
    # Get the player
    player = Player.query.filter_by(id=player_id).first()

    # Verify the player creation inputs
    if player:

        # Get the input validator
        inputs = UpdateInputs(request.values)

        if inputs.validate_on_submit():

            try:
                player.update(**request.values.to_dict())
                return jsonify(player.serialized), 200
            except Exception as e:
                return jsonify({'errors': {e.__class__.__name__: [e.message]}, 'inputs': inputs.obfuscated()}), 422

        combined_inputs = dict(inputs.obfuscated().items() + {'id': player_id}.items())
        return jsonify({'errors': inputs.errors, 'inputs': combined_inputs}), 422

    return jsonify({'errors': NOT_FOUND_ERROR, 'inputs': {'id': player_id}}), 422


# Set the route and accepted methods
@players_module.route('/<int:player_id>', methods=['DELETE'])
def delete(player_id):
    # Get the player
    player = Player.query.filter_by(id=player_id).first()

    # Verify the player creation inputs
    if player:
        try:
            player.update(**{'active': False})
            return jsonify(player.serialized), 200
        except Exception as e:
            return jsonify({'errors': {e.__class__.__name__: [e.message]}}), 422

    return jsonify({'errors': NOT_FOUND_ERROR, 'inputs': {'id': player_id}}), 422


# Set the route and accepted methods
@players_module.route('/signin/', methods=['POST'])
def signin():
    # Get the input validator
    inputs = SignInInputs(request.values)

    # Verify the sign in inputs
    if inputs.validate_on_submit():

        player = Player.query.filter_by(username=inputs.username.data).first()

        if player and check_password_hash(player.password, inputs.password.data):

            if login_user(player):
                return jsonify(player.serialized.items()), 200
            else:
                return jsonify({'errors': UNABLE_TO_SIGNIN_ERROR, 'inputs': inputs.obfuscated()}), 422

        jsonify({'errors': INVALID_USERNAME_PASSWORD_ERROR, 'inputs': inputs.obfuscated()}), 422

    return jsonify({'errors': inputs.errors, 'inputs': inputs.obfuscated()}), 422
