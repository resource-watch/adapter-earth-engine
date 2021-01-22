import logging

from RWAPIMicroservicePython import request_to_microservice

from adapterearthengine.errors import SqlFormatError


def convert(query, query_type='sql'):
    if not query:
        raise SqlFormatError(message='sql or fs not provided')
    if query_type == 'fs' and '&' not in query:
        raise SqlFormatError(message='sql or fs not provided')

    logging.info('Converting Query: ' + query)

    endpoint = 'sql2SQL'
    if query_type == 'fs':
        endpoint = 'fs2SQL'

    result = endpoint + query
    logging.info(f'[QUERY SERVICE - convert]: {result}')

    try:
        config = {
            'uri': '/convert/' + result,
            'method': 'GET'
        }
        response = request_to_microservice(config)
        return response
    except Exception as error:
        raise error

    if response.get('errors'):
        errors = response.get('errors')
        raise SqlFormatError(message=errors[0].get('detail'))


def get_geojson(geostore):
    try:
        config = {
            'uri': f'/geostore/{geostore}',
            'method': 'GET'
        }
        response = request_to_microservice(config)
        return response.get('data').get('attributes').get('geojson')
    except Exception as error:
        raise error

    if response.get('errors'):
        errors = response.get('errors')
        raise SqlFormatError(message=errors[0].get('detail'))


def get_type(table_name):
    logging.info('Getting Dataset Type')

    if 'ft:' in table_name:
        return 'ft'
    else:
        return 'raster'


def get_clone_url(dataset_id, query):
    return {
        'httpMethod': 'POST',
        'url': '/v1/dataset/' + dataset_id + '/clone',
        'body': {
            'dataset': {
                'datasetUrl': '/query/' + dataset_id + '?sql=' + query,
                'application': [
                    'your',
                    'apps'
                ]
            }
        }
    }
