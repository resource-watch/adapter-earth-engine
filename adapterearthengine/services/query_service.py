import logging
import re

from adapterearthengine.responders import QueryResponder
from adapterearthengine.utils.http import request_to_microservice
from adapterearthengine.errors import SqlFormatError


def convert(query, type='sql'):
    logging.info('Converting Query')

    if not query:
        raise SqlFormatError(message='sql or fs not provided')

    query_type = 'sql2SQL?sql='+query
    if type == 'fs':
        query_type = 'fs2SQL' # @TODO

    try:
        config = {
            'uri': '/convert/'+query_type,
            'method': 'GET'
        }
        response = request_to_microservice(config)
    except Exception as error:
        raise error

    if response.get('errors'):
        errors = response.get('errors')
        raise SqlFormatError(message=errors[0].get('detail'))

    query = QueryResponder().deserialize(response)
    query = query.get('attributes', {}).get('query')
    #return quote_table(query, type)
    return query


def quote_table(query, type='sql'):
    regex = re.compile(r'from ([a-zA-Z0-9_:-]*)', re.IGNORECASE)
    table = regex.search(query).group(1)
    if get_type(table) is 'ft':
        query = query.replace(table, '\"'+table+'\"')
    return query


def get_geojson(geostore_id):
    logging.info('Getting Geojson')
    try:
        config = {
            'uri': '/geostore/'+geostore_id,
            'method': 'GET'
        }
        response = request_to_microservice(config)
    except Exception as error:
        raise error

    if response.get('errors'):
        errors = response.get('errors')
        raise GeojsonNotFound(message=errors[0].get('detail'))

    return response.get('data', {}).get('attributes')


def get_type(table_name):
    logging.info('Getting Dataset Type')

    if 'ft:' in table_name:
        return 'ft'
    else:
        return 'raster'


def get_clone_url(dataset_id):
    return {
        'httpMethod': 'POST',
        'url': '/dataset/'+dataset_id,
        'body': {
            'dataset': {
                'datasetUrl': '/query/'+dataset_id,
                'application': [
                    'your',
                    'apps'
                ]
            }
        }
    }
