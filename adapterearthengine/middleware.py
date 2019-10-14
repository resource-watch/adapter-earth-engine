import json
import logging
from functools import wraps

from flask import request
from adapterearthengine.routes.api import error


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
