# Import flask and template operators
from flask import Flask

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Import view rendering
from application.controllers import render_view

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_view('404', 404, errors={error.__class__.__name__: [error.message]})

# Import a module / component using its blueprint handler variable
from application.controllers.Players import players_module
from application.controllers.Games import games_module
from application.controllers.Matches import matches_module

# Register blueprint(s)
app.register_blueprint(players_module)
app.register_blueprint(games_module)
app.register_blueprint(matches_module)

# Build the database:
# This will create the database file using SQLAlchemy
# TODO replace sqlite with mysql
db.create_all()

# Configure the logger to print all SQL statements, if requested
if app.config.get('PRINT_SQL', False):
    import logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

logging.getLogger('werkzeug').setLevel(logging.INFO)