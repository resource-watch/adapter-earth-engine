import logging

from adapterearthengine.errors import GEEQueryError
from sql2gee import SQL2GEE


def execute_query(json_sql, geojson=None, flags=None):
    logging.info('Executing Query')

    try:
        return SQL2GEE(sql=json_sql, geojson=geojson, flags=None)
    except Exception as error:
        raise GEEQueryError(error)
