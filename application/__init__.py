import logging

# Import flask and template operators
from flask import Flask

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported by model and controllers
db = SQLAlchemy(app)

# Import view rendering
from application.controllers import render_view

# Specify 404 error handling
@app.errorhandler(404)
def not_found(error):
    return render_view('404', 404, errors={error.__class__.__name__: [error.message]})

# Import a module / component using its blueprint handler variable
from application.controllers.Players import players_module
from application.controllers.Games import games_module
from application.controllers.Matches import matches_module
from application.controllers.Words import words_module
from application.controllers.DefinitionTemplates import definition_templates_module
from application.controllers.DefinitionFillers import definition_fillers_module

# Register blueprints
app.register_blueprint(players_module)
app.register_blueprint(games_module)
app.register_blueprint(matches_module)
app.register_blueprint(words_module)
app.register_blueprint(definition_templates_module)
app.register_blueprint(definition_fillers_module)

# Build the database:
# This will create the database using SQLAlchemy
db.create_all()

logging.basicConfig()
logging.getLogger('werkzeug').setLevel(logging.INFO)

# Configure the logger to print all SQL statements, if requested
if app.config.get('PRINT_SQL', False):
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)