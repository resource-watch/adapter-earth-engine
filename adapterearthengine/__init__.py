import os
import json
import logging
import ee
from oauth2client.service_account import ServiceAccountCredentials

from flask import Flask
from adapterearthengine.config import settings
from adapterearthengine.routes.api.v1 import endpoints
from adapterearthengine.utils.files import load_config_json
import CTRegisterMicroserviceFlask

# Logging
logging.basicConfig(
    level = settings.get('logging', {}).get('level'),
    format = '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
    datefmt = '%Y%m%d-%H:%M%p',
)

# Initializing GEE
gee = settings.get('gee')
gee_credentials = ServiceAccountCredentials.from_p12_keyfile(
    gee.get('service_account'),
    gee.get('privatekey_file'),
    scopes = ee.oauth.SCOPE
 )

ee.Initialize(gee_credentials)

def create_application():
    # Flask
    application = Flask(__name__)

    # Config
    application.config.from_object(settings)

    # Routing
    application.register_blueprint(endpoints, url_prefix='/api/v1/earthengine')

    # CT
    info = load_config_json('register')
    swagger = load_config_json('swagger')
    CTRegisterMicroserviceFlask.register(
        app = application,
        name = 'adapter-earth-engine',
        info = info,
        swagger = swagger,
        mode = CTRegisterMicroserviceFlask.AUTOREGISTER_MODE,
        ct_url = os.getenv('CT_URL'),
        url = os.getenv('LOCAL_URL')
    )

    return application
