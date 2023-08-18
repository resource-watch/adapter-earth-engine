import logging
import os
import httplib2

import RWAPIMicroservicePython
import ee
from flask import Flask

from adapterearthengine.config import SETTINGS
from adapterearthengine.routes.api import error
from adapterearthengine.routes.api.v1 import earth_engine_endpoints

# Logging
logging.basicConfig(
    level=SETTINGS.get('logging', {}).get('level'),
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
    datefmt='%Y%m%d-%H:%M%p',
)

EE_ACCOUNT = os.environ['EE_ACCOUNT']
EE_PRIVATE_KEY_FILE = 'privatekey.json'

gee_credentials = ee.ServiceAccountCredentials(EE_ACCOUNT, EE_PRIVATE_KEY_FILE)

ee.Initialize(gee_credentials, http_transport=httplib2.Http())
ee.data.setDeadline(60000)

# Flask
app = Flask(__name__)

# Config
app.config.from_object(SETTINGS)

# Routing
app.register_blueprint(earth_engine_endpoints, url_prefix='/api/v1/earthengine')

RWAPIMicroservicePython.register(
    app=app,
    gateway_url=os.getenv("GATEWAY_URL"),
    token=os.getenv("MICROSERVICE_TOKEN"),
    aws_cloud_watch_logging_enabled=(
        os.getenv("AWS_CLOUD_WATCH_LOGGING_ENABLED", "True").lower() == "true"
    ),
    aws_cloud_watch_log_stream_name=SETTINGS.get("service", {}).get("name"),
    aws_region=os.getenv("AWS_REGION"),
    require_api_key=(os.getenv("REQUIRE_API_KEY", "False").lower() == "true"),
)


@app.errorhandler(403)
def forbidden(e):
    logging.error('Forbidden')
    return error(status=403, detail='Forbidden')


@app.errorhandler(404)
def page_not_found(e):
    logging.error('Not Found')
    return error(status=404, detail='Not Found')


@app.errorhandler(405)
def method_not_allowed(e):
    logging.error('Method Not Allowed')
    return error(status=405, detail='Method Not Allowed')


@app.errorhandler(410)
def gone(e):
    logging.error('Gone')
    return error(status=410, detail='Gone')


@app.errorhandler(500)
def internal_server_error(e):
    logging.error('Internal Server Error')
    return error(status=500, detail='Internal Server Error')
