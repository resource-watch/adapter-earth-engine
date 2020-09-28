import logging

from sql2gee import SQL2GEE

from adapterearthengine.errors import GEEQueryError


def execute_query(json_sql, geojson=None, flags=None):
    logging.info('Executing Query')
    logging.info(json_sql)
    try:
        return SQL2GEE(json_sql, geojson, flags)
    except Exception as error:
        raise GEEQueryError(str(error))
