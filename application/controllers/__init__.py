from flask import render_template, request, g
from functools import wraps

from werkzeug.datastructures import MultiDict

from application.models.Player import Player
from application import app


UNAUTHORIZED_ERROR = {'UnauthorizedAccess': ['Attempted to access data without an authenticated player']}


def get_inputs():
    if request.content_type == 'application/json' and request.method != 'GET':
        return MultiDict(dict(request.get_json(force=True).items() + request.values.items()))
    else:
        return request.values


def render_view(template, code, **variables):
    if request.content_type == 'application/json':
        return render_template_type(template, 'json', code, 'application/json', variables)
    else:
        variables['user_logged_in'] = g.user_logged_in
        return render_template_type(template, 'html', code, 'text/html', variables)


def render_template_type(template, extension, code, content_type, variables):
    return (
        render_template('{}.{}'.format(template, extension), **variables),
        code,
        {'Content-Type': '{}; charset=utf-8'.format(content_type)}
    )


def get_current_user():
    if hasattr(g, 'current_user'):
        return g.current_user
    return None


def set_current_user(current_user):
    g.current_user = current_user


def get_user_logged_in():
    if hasattr(g, 'user_logged_in'):
        return g.user_logged_in
    return None


def set_user_logged_in(user_logged_in):
    g.user_logged_in = user_logged_in


# Set the route and accepted methods
@app.route('/', methods=['GET'])
def index():
    return render_view('index', 200)


# Define the before_request functionality for login
@app.before_request
def before_request():
    params = get_inputs()
    if params.get('auth_token'):
        player = Player.get_from_auth(params.get('auth_token'))
        if player:
            set_current_user(player)
            set_user_logged_in(True)


def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not get_current_user():
            return render_view('422', 422, errors=UNAUTHORIZED_ERROR)

        return f(*args, **kwargs)

    return wrapper
