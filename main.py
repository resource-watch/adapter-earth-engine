import os
from adapterearthengine import create_application

application = create_application()

# This is only used when running locally. When running live, Gunicorn runs
# the application.
if __name__ == '__main__':
    application.run(
        host = '0.0.0.0',
        port = int(os.environ['PORT']),
        debug = os.environ['DEBUG'] == 'True'
    )
