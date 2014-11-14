# Run a test server.
from application import app
app.run(host=app.config.get('HOST'), port=app.config.get('PORT'), debug=app.config.get('DEBUG'))
