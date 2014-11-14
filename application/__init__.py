# Import flask and template operators
from flask import Flask, jsonify

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Import Flask-Login
from flask.ext.login import LoginManager

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Define the login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({"errors": {error.__class__.__name__: [error.message]}}), 404

# Import a module / component using its blueprint handler variable
from application.controllers.Players import players_module

# Register blueprint(s)
app.register_blueprint(players_module)

# Build the database:
# This will create the database file using SQLAlchemy
# TODO replace sqlite with mysql
db.create_all()
