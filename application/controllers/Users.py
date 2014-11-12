# Import flask dependencies
from flask import Blueprint, request, jsonify, session
from flask.ext.login import login_user

# Import password / encryption helper tools
from werkzeug.security import generate_password_hash, check_password_hash

# Import input validators
from application.inputs.Users import ListInputs, CreateInputs, UpdateInputs, SignInInputs

# Import models
from application.models.User import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
users_module = Blueprint('users', __name__, url_prefix='/users')

# Set some common error constants
NOT_FOUND_ERROR = {'NotFound': ['Unable to find User']}
INVALID_USERNAME_PASSWORD_ERROR = {'InvalidInputs': ['Wrong username or password']}
UNABLE_TO_SIGNIN_ERROR = {'SigninError': ['Unable to sign in an inactive user']}


# Set the route and accepted methods
@users_module.route('/', methods=['GET'])
def index():

    # Get the input validator
    inputs = ListInputs(request.values)

    # Verify the list inputs
    if inputs.validate():

        users = User.query.order_by(User.id).limit(inputs.limit.data).offset(inputs.offset.data).all()

        return jsonify({user.id: user.serialized for user in users}), 200

    return jsonify({'errors': inputs.errors, 'inputs': inputs.obfuscated()}), 422


# Set the route and accepted methods
@users_module.route('/', methods=['POST'])
def create():

    # Get the input validator
    inputs = CreateInputs(request.values)

    # Verify the user creation inputs
    if inputs.validate_on_submit():

        user = User(inputs.username.data, generate_password_hash(inputs.password.data))
        try:
            user.save()
            return jsonify(user.serialized), 201
        except Exception as e:
            return jsonify({'errors': {e.__class__.__name__: [e.message]}, 'inputs': inputs.obfuscated()}), 422

    return jsonify({'errors': inputs.errors, 'inputs': inputs.obfuscated()}), 422


# Set the route and accepted methods
@users_module.route('/<int:user_id>', methods=['GET'])
def get(user_id):

    # Get the user
    user = User.query.filter_by(id=user_id).first()

    if user:
        return jsonify(user.serialized), 200

    return jsonify({'errors': NOT_FOUND_ERROR, 'inputs': {'id': user_id}}), 422


# Set the route and accepted methods
@users_module.route('/<int:user_id>', methods=['PUT'])
def update(user_id):

    # Get the user
    user = User.query.filter_by(id=user_id).first()

    # Verify the user creation inputs
    if user:

        # Get the input validator
        inputs = UpdateInputs(request.values)

        if inputs.validate_on_submit():

            try:
                user.update(**request.values.to_dict())
                return jsonify(user.serialized), 200
            except Exception as e:
                return jsonify({'errors': {e.__class__.__name__: [e.message]}, 'inputs': inputs.obfuscated()}), 422

        combined_inputs = dict(inputs.obfuscated().items() + {'id': user_id}.items())
        return jsonify({'errors': inputs.errors, 'inputs': combined_inputs}), 422

    return jsonify({'errors': NOT_FOUND_ERROR, 'inputs': {'id': user_id}}), 422


# Set the route and accepted methods
@users_module.route('/<int:user_id>', methods=['DELETE'])
def delete(user_id):

    # Get the user
    user = User.query.filter_by(id=user_id).first()

    # Verify the user creation inputs
    if user:
        try:
            user.update(**{'active': False})
            return jsonify(user.serialized), 200
        except Exception as e:
            return jsonify({'errors': {e.__class__.__name__: [e.message]}}), 422

    return jsonify({'errors': NOT_FOUND_ERROR, 'inputs': {'id': user_id}}), 422


# Set the route and accepted methods
@users_module.route('/signin/', methods=['POST'])
def signin():

    # Get the input validator
    inputs = SignInInputs(request.values)

    # Verify the sign in inputs
    if inputs.validate_on_submit():

        user = User.query.filter_by(username=inputs.username.data).first()

        if user and check_password_hash(user.password, inputs.password.data):

            if login_user(user):
                return jsonify(user.serialized.items()), 200
            else:
                return jsonify({'errors': UNABLE_TO_SIGNIN_ERROR, 'inputs': inputs.obfuscated()}), 422

        jsonify({'errors': INVALID_USERNAME_PASSWORD_ERROR, 'inputs': inputs.obfuscated()}), 422

    return jsonify({'errors': inputs.errors, 'inputs': inputs.obfuscated()}), 422
