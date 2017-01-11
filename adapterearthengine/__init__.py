import json
import logging

from flask import Flask
from adapterearthengine.routes.api.v1 import endpoints
from adapterearthengine.config import settings

# Logging
logging.basicConfig(
    level = settings.get('logging', {}).get('level'),
    format = '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
    datefmt = '%Y%m%d-%H:%M%p',
)

def create_application():

    # Flask
    app = Flask(__name__)

    app.config.from_object(settings)
    
    # Routing
    app.register_blueprint(endpoints, url_prefix='/api/v1')

    return app
