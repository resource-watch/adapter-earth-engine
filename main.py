import os
from adapterearthengine import create_application

app = create_application()

# This is only used when running locally. When running live, uWSGI runs
# the application.
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ['PORT']),
        debug=os.environ['DEBUG'] == 'True'
    )
