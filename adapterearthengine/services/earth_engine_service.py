import logging

from adapterearthengine.errors import GEEQueryError
from sql2gee import SQL2GEE


def query(query, geojson=None):
    logging.info('Executing Query: '+query)

    try:
        q = SQL2GEE(sql=query, geojson=geojson, flags=None)
        response = q.response
    except Exception as error:
        raise GEEQueryError(error)

    return response
