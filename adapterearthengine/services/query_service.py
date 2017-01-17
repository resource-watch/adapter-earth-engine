import logging

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
    return query.get('query')
