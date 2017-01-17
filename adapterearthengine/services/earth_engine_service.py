import logging

from adapterearthengine.errors import GEEQueryError
from sql2gee import SQL2GEE


def query(query):
    logging.info('Executing Query: '+query)

    try:
        response = SQL2GEE(query).execute()
    except Exception as error:
        raise GEEQueryError(error)

    return response


def fields():
    pass


def download():
    pass
