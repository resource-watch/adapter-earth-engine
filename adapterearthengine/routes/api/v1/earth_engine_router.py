import json
import csv
import copy
import logging

from flask import jsonify, request, Response, stream_with_context, Blueprint
from CTRegisterMicroserviceFlask import request_to_microservice

from adapterearthengine.routes.api import error
from adapterearthengine.services import EarthEngineService, QueryService
from adapterearthengine.errors import SqlFormatError, GEEQueryError, GeojsonNotFound
from adapterearthengine.serializers import serialize_query, serialize_fields

earth_engine_endpoints = Blueprint('endpoints', __name__)


def build_query(rq):
    dataset = rq.get_json().get('dataset').get('data')
    sql = rq.args.get('sql', None) or rq.get_json().get('sql', None)
    logging.info(f'[ROUTER build_query]: {str(rq.args)}')
    # sql or fs
    if sql:
        test = copy.deepcopy(rq.args).to_dict() or copy.deepcopy(rq.get_json()).to_dict()
        result_query = f'?sql={sql}'
    else:
        fs = copy.deepcopy(rq.args) or copy.deepcopy(rq.get_json())

        if fs.get('dataset'):
            del fs['dataset']

        result_query = '?tableName="' + dataset.get('attributes', None).get('tableName') + '"'
        for key in fs.keys():
            param = '&' + key + '=' + fs.get(key)
            result_query += param
    return result_query


@earth_engine_endpoints.route('/query/<dataset_id>', methods=['POST'])
def query(dataset_id):
    """Query GEE Dataset Endpoint"""
    logging.info('Doing GEE Query')
    sql = request.args.get('sql', None) or request.get_json().get('sql', None)
    geostore = request.args.get('geostore', None) or request.get_json().get('geostore', None)
    result_query = build_query(request)

    try:
        if sql:
            query_type = 'sql'
        else:
            query_type = 'fs'
        json_sql = QueryService.convert(result_query, query_type=query_type)
        
    except SqlFormatError as e:
        logging.error('[ROUTER] /query/<dataset_id> - SQL Format error in query conversion: '+e.message)
        return error(status=400, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER] /query/<dataset_id> - Generic error in query conversion: '+str(e))
        return error(status=500, detail='Generic Error')

    try:
        if geostore:
            geojson = QueryService.get_geojson(geostore)
        else:
            geojson = None
        response = EarthEngineService.execute_query(json_sql, geojson).response()
    except GEEQueryError as e:
        logging.error('[ROUTER] /query/<dataset_id> - GEE Query error in GEE query execution: '+e.message)
        return error(status=400, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER] /query/<dataset_id> - Generic error in GEE query execution: '+str(e))
        return error(status=500, detail='Generic Error')

    # @TODO
    meta = {}
    return jsonify(serialize_query(response, meta)), 200


@earth_engine_endpoints.route('/fields/<dataset_id>', methods=['POST'])
def fields(dataset_id):
    """Get GEE Dataset Fields Endpoint"""
    logging.info('Getting fields of a GEE Dataset')

    dataset = request.get_json().get('dataset').get('data')
    table_name = dataset.get('attributes').get('tableName')
    sql = '?sql=SELECT * FROM \"' + table_name + '\" LIMIT 1'

    # Convert query
    json_sql = QueryService.convert(sql, query_type='sql')

    try:
        response = EarthEngineService.execute_query(json_sql).metadata
    except GEEQueryError as e:
        logging.error('[ROUTER] /fields/<dataset_id> - GEE Query error in GEE query execution: '+e.message)
        return error(status=400, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER] /fields/<dataset_id> - Generic error in GEE query execution: '+str(e))
        return error(status=500, detail='Generic Error')

    return jsonify(data=serialize_fields(response, table_name)), 200


@earth_engine_endpoints.route('/download/<dataset_id>', methods=['POST'])
def download(dataset_id):
    """Download GEE Dataset Endpoint"""
    logging.info('Downloading GEE Dataset')

    sql = request.args.get('sql', None) or request.get_json().get('sql', None)
    result_query = build_query(request)

    try:
        if sql:
            query_type = 'sql'
        else:
            query_type = 'fs'
        json_sql = QueryService.convert(result_query, query_type=query_type)
    except SqlFormatError as e:
        logging.error('[ROUTER] /download/<dataset_id> - SQL Format error in query conversion: '+e.message)
        return error(status=400, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER] /download/<dataset_id> - Generic error in query conversion: '+str(e))
        return error(status=500, detail='Generic Error')

    try:
        response = EarthEngineService.execute_query(json_sql).response()
    except GEEQueryError as e:
        logging.error('[ROUTER] /download/<dataset_id> - GEE Query error in GEE query execution: '+e.message)
        return error(status=400, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER] /download/<dataset_id> - Generic error in GEE query execution: '+str(e))
        return error(status=500, detail='Generic Error')

    # @TODO
    meta = {}
    # @TODO download content-type
    return jsonify(data=serialize_query(response, meta)), 200


@earth_engine_endpoints.route('/rest-datasets/gee', methods=['POST'])
def register_dataset():
    """Register GEE Dataset Endpoint"""
    logging.info('Registering new GEE Dataset')

    table_name = request.get_json().get('connector').get('table_name')
    sql = '?sql=SELECT * FROM \"' + table_name + '\" LIMIT 1'

    # Convert query
    json_sql = QueryService.convert(sql, query_type='sql')

    try:
        response = EarthEngineService.execute_query(json_sql).metadata
        status = 1
    except GEEQueryError as e:
        logging.error('[ROUTER] /rest-datasets/gee - GEE Query error in GEE query execution: '+e.message)
        status = 2
    except Exception as e:
        logging.error('[ROUTER] /rest-datasets/gee - Generic error in GEE query execution: '+str(e))
        status = 2

    config = {
        'uri': '/dataset/'+request.get_json().get('connector').get('id'),
        'method': 'PATCH',
        'body': {'status': status}
    }
    response = request_to_microservice(config)
    return jsonify(data=serialize_fields(response, table_name)), 200
