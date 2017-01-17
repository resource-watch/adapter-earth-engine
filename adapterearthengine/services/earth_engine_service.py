import logging

from adapterearthengine.errors import GEEQueryError
from sql2gee import SQL2GEE


def query(query):
    logging.info('Executing Query: '+query)

    try:
        q = SQL2GEE(query)
        response = q.execute()
    except Exception as error:
        raise GEEQueryError(error)

    return response
