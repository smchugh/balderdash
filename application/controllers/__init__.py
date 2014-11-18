from flask import render_template, request, g
from functools import wraps

from werkzeug.datastructures import MultiDict, ImmutableMultiDict, CombinedMultiDict

from application.models.Player import Player
from application import app


UNAUTHORIZED_ERROR = {'UnauthorizedAccess': ['Attempted to access data without an authenticated player']}


def is_json_input_valid():
    return request.content_type == 'application/json' and request.method != 'GET'


def get_inputs():
    if is_json_input_valid():
        return MultiDict(dict(request.get_json(force=True).items() + request.values.items()))
    else:
        return request.values


def unset_input(key):
    if key in request.args:
        request.args = rebuild_immutable_multidict_without_key(request.args, key)
        request.values = build_combined_multidict(request.args, request.form)
    if key in request.form:
        request.form = rebuild_immutable_multidict_without_key(request.form, key)
        request.values = build_combined_multidict(request.args, request.form)
    if is_json_input_valid() and key in request.json:
        del request.json[key]


def build_combined_multidict(multidict1, multidict2):
    args = []
    for d in multidict1, multidict2:
        if not isinstance(d, MultiDict):
            d = MultiDict(d)
        args.append(d)
    return CombinedMultiDict(args)


def rebuild_immutable_multidict_without_key(multidict, key):
    tmp = MultiDict(multidict)
    del tmp[key]
    return ImmutableMultiDict(tmp)


def get_mixed_dict_from_multidict(multidict, inputs=None):
        """
        Returns a dictionary where the values are either single
        values, or a list of values when a key/value appears more than
        once in this dictionary.  This is similar to the kind of
        dictionary often used to represent the variables in a web
        request.
        """
        result = {}
        for item in multidict.lists():
            key = item[0]
            if len(item[1]) == 1 and inputs and not isinstance(inputs.data.get(key), list):
                value = item[1][0]
            else:
                value = item[1]

            result[key] = value

        return result


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
            unset_input('auth_token')


def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not get_current_user():
            return render_view('422', 422, errors=UNAUTHORIZED_ERROR)

        return f(*args, **kwargs)

    return wrapper
