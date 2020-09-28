from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from flask import jsonify


def error(status=500, detail='Generic Error'):
    error = {
        'status': status,
        'detail': detail
    }
    return jsonify(errors=[error]), status
