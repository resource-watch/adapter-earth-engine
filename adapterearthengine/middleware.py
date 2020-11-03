import json
import logging
from functools import wraps

from flask import request

from adapterearthengine.routes.api import error
from adapterearthengine.services.dataset_service import DatasetService
from adapterearthengine.errors import DatasetNotFound


def is_microservice_or_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.debug("Checking microservice user")
        logged_user = json.loads(request.args.get("loggedUser", None))
        if (logged_user.get("id") == "microservice") or (logged_user.get("role") == "ADMIN"):
            logging.debug("is microservice or admin");
            return func(*args, **kwargs)
        else:
            return error(status=403, detail="Not authorized")

    return wrapper


def get_dataset_from_id(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.debug("Getting dataset from id")
        logging.debug("Getting dataset from id")

        try:
            dataset_object = DatasetService.get(kwargs['dataset_id'])
        except DatasetNotFound:
            return error(status=404, detail="Dataset with id {} doesn't exist".format(kwargs['dataset_id']))

        connector_type = dataset_object.get('connectorType', None)
        provider = dataset_object.get('provider', None)

        if connector_type != "rest":
            return error(status=422, detail="This operation is only supported for datasets with connectorType 'rest'")

        if provider != "gee":
            return error(status=422, detail="This operation is only supported for datasets with provider 'gee'")

        kwargs['dataset'] = dataset_object

        return func(*args, **kwargs)

    return wrapper
