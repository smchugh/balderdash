from flask import render_template, request
from flask.ext.login import user_logged_in

from werkzeug.datastructures import MultiDict

from application.models.Player import Player
from application import app, login_manager

@login_manager.user_loader
def load_user(user_id):
    return Player.get(user_id)


def get_inputs():
    if request.content_type == 'application/json' and request.method != 'GET':
        return MultiDict(dict(request.get_json(force=True).items() + request.values.items()))
    else:
        return request.values


def render_view(template, code, **variables):
    if request.content_type == 'application/json':
        return render_template_type(template, 'json', code, 'application/json', variables)
    else:
        variables['user_logged_in'] = user_logged_in
        return render_template_type(template, 'html', code, 'text/html', variables)


def render_template_type(template, extension, code, content_type, variables):
    return (
        render_template('{}.{}'.format(template, extension), **variables),
        code,
        {'Content-Type': '{}; charset=utf-8'.format(content_type)}
    )

# Set the route and accepted methods
@app.route('/', methods=['GET'])
def index():
    return render_view('index', 200)