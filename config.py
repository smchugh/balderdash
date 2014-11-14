import os

# Statement for enabling the development environment
DEBUG = True
PRINT_SQL = os.environ.get('PRINT_SQL', False) in [True, 'True', '1', 'y', 'yes']

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = False
WTF_CSRF_ENABLED = False

# Use a secure, unique and absolutely secret key for signing the data.
CSRF_SESSION_KEY = "16da308e5a1c605eb9878939293808bc"
WTF_CSRF_SECRET_KEY = "16da308e5a1c605eb9878939293808bc"

# Secret key for signing cookies
SECRET_KEY = "16da308e5a1c605eb9878939293808bc"

# Application run-time configs
PORT = 8080
HOST = '0.0.0.0'

# Environment specific config overrides
APPLICATION_ENV = os.environ.get('APPLICATION_ENV', 'dev')
if APPLICATION_ENV == 'dev':
    PORT = 8181
elif APPLICATION_ENV == 'staging':
    pass
elif APPLICATION_ENV == 'production':
    pass