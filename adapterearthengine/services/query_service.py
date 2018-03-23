import logging
import re

from CTRegisterMicroserviceFlask import request_to_microservice

from adapterearthengine.errors import SqlFormatError


def convert(query, query_type='sql'):
    if not query:
        raise SqlFormatError(message='sql or fs not provided')
    if query_type == 'fs' and not '&' in query:
        raise SqlFormatError(message='sql or fs not provided')

    logging.info('Converting Query: '+query)

    endpoint = 'sql2SQL'
    if query_type == 'fs':
        endpoint = 'fs2SQL'

    result = endpoint+query

    try:
        config = {
            'uri': '/convert/'+result,
            'method': 'GET'
        }
        response = request_to_microservice(config)
        return response
    except Exception as error:
        raise error

    if response.get('errors'):
        errors = response.get('errors')
        raise SqlFormatError(message=errors[0].get('detail'))


def quote_table(query, type='sql'):
    regex = re.compile(r'from ([a-zA-Z0-9_:-]*)', re.IGNORECASE)
    table = regex.search(query).group(1)
    if get_type(table) is 'ft':
        query = query.replace(table, '\"'+table+'\"')
    return query


def get_geojson(json_sql):

    where = json_sql.get('where', None)
    if where:
        firstnode = where

    def check_node(node):
        if node.get('type') == 'function' and node.get('value') == 'ST_INTERSECTS':
            st_intersects_arguments = node.get('arguments')[0]
            if st_intersects_arguments.get('type') == 'function' and st_intersects_arguments.get('value') == 'ST_SetSRID':
                st_setsrid_arguments = st_intersects_arguments.get('arguments')[0]
                if st_setsrid_arguments.get('type') == 'function' and st_setsrid_arguments.get('value') == 'ST_GeomFromGeoJSON':
                    st_geomfromgeojson_arguments = st_setsrid_arguments.get('arguments')[0]
                    return st_geomfromgeojson_arguments
        else:
            return check_node(node.get('arguments'))

    geojson = check_node(firstnode)
    geojson = geojson.get('value')
    return geojson


def get_type(table_name):
    logging.info('Getting Dataset Type')

    if 'ft:' in table_name:
        return 'ft'
    else:
        return 'raster'


def get_clone_url(dataset_id, query):
    return {
        'httpMethod': 'POST',
        'url': '/v1/dataset/'+dataset_id+'/clone',
        'body': {
            'dataset': {
                'datasetUrl': '/query/'+dataset_id+'?sql='+query,
                'application': [
                    'your',
                    'apps'
                ]
            }
        }
    }
