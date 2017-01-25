import os
import json
import csv
import StringIO
import logging

from flask import jsonify, request, Response
import requests

from . import endpoints
from adapterearthengine.responders import ErrorResponder, DatasetResponder, QueryResponder, FieldsResponder
from adapterearthengine.services import EarthEngineService, QueryService
from adapterearthengine.errors import SqlFormatError, GEEQueryError
from adapterearthengine.utils.http import request_to_microservice

@endpoints.route('/query/<dataset_id>', methods=['POST'])
def query(dataset_id):
    """Query GEE Dataset Endpoint"""
    logging.info('Doing GEE Query')

    # Get and deserialize
    dataset = DatasetResponder().deserialize(request.get_json())
    sql = request.args.get('sql', None) or request.get_json().get('sql', None)
    fs = request.args.get('fs', None) or request.get_json().get('fs', None)

    if not sql and not fs:
        response = ErrorResponder.build({
            'status': 400,
            'message': 'sql or fs param is required'
        })
        return jsonify(response), 400

    # Query format and query to GEE
    try:
        if fs:
            query = QueryService.convert(fs, type='fs')
        else:
            query = QueryService.convert(sql, type='sql')
        response = EarthEngineService.query(query)
    except SqlFormatError as error:
        logging.error(error.message)
        response = ErrorResponder.build({'status': 400, 'message': error.message})
        return jsonify(response), 400
    except GEEQueryError as error:
        logging.error(error.message)
        response = ErrorResponder.build({'status': 500, 'message': error.message})
        return jsonify(response), 500
    except Exception as error:
        response = ErrorResponder.build({'status': 500, 'message': 'Generic Error'})
        return jsonify(response), 500

    if type(response) is int or type(response) is float:
        response = QueryResponder.build({'result': float(response)})
        return jsonify(response), 200

    response = QueryResponder().serialize(response.get('features', {}))
    response = QueryResponder.build({'attributes': response})
    return jsonify(response), 200


@endpoints.route('/fields/<dataset_id>', methods=['POST'])
def fields(dataset_id):
    """Get GEE Dataset Fields Endpoint"""
    logging.info('Getting fields of a GEE Dataset')

    # Get and deserialize
    dataset = DatasetResponder().deserialize(request.get_json())

    # Build query
    table_name = dataset.get('attributes').get('tableName')
    sql = 'SELECT * FROM ' + table_name + ' LIMIT 1'

    # Convert query
    query = QueryService.convert(sql, type='sql')

    try:
        response = EarthEngineService.query(query)
    except GEEQueryError as error:
        logging.error(error.message)
        response = ErrorResponder.build({'status': 500, 'message': error.message})
        return jsonify(response), 500

    fields = FieldsResponder().serialize(response.get('columns', {}))
    response = FieldsResponder.build({'tableName': table_name, 'fields': fields})
    return jsonify(response), 200


@endpoints.route('/download/<dataset_id>', methods=['POST'])
def download(dataset_id):
    """Download GEE Dataset Endpoint"""
    logging.info('Downloading GEE Dataset')

    # Get and deserialize
    dataset = DatasetResponder().deserialize(request.get_json())
    sql = request.args.get('sql', None) or request.get_json().get('sql', None)
    fs = request.args.get('fs', None) or request.get_json().get('fs', None)

    if not sql and not fs:
        response = ErrorResponder.build({
            'status': 400,
            'message': 'sql or fs param is required'
        })
        return jsonify(response), 400

    # Query format and query to GEE
    try:
        if fs:
           query = QueryService.convert(fs, type='fs')
        else:
           query = QueryService.convert(sql, type='sql')
        response = EarthEngineService.query(query)
    except SqlFormatError as error:
        logging.error(error.message)
        response = ErrorResponder.build({'status': 400, 'message': error.message})
        return jsonify(response), 500
    except GEEQueryError as error:
        logging.error(error.message)
        response = ErrorResponder.build({'status': 500, 'message': error.message})
        return jsonify(response), 500
    except:
        response = ErrorResponder.build({'status': 500, 'message': 'Generic Error'})
        return jsonify(response), 500

    if type(response) is int or type(response) is float:
        features = [float(response)]
    else:
        features = QueryResponder().serialize(response.get('features', {}))

    f_len = len(features)

    def generate_csv():
        si = StringIO.StringIO()
        writer = csv.writer(si)
        for idx, feature in enumerate(features):
            if idx == 0:
                writer.writerow(feature.keys())
            else:
                writer.writerow(feature.values())
        yield si.getvalue() # @TODO Stream Response

    def generate_json():
        yield '{"data": ['
        for idx, feature in enumerate(features):
            if idx != f_len-1:
                yield json.dumps(feature) + ', '
            else:
                yield json.dumps(feature)
        yield ']}'

    format = request.args.get('format', None)
    if format == 'csv':
        return Response(generate_csv(),
            mimetype='text/csv',
            headers={
                'Content-Disposition': 'attachment; filename=export.csv',
                'Content-type': 'text/csv'
            }
        )
    else:
        return Response(generate_json(),
            mimetype='application/json',
            headers={
                'Content-Disposition': 'attachment; filename=export.json',
                'Content-type': 'application/json'
            }
        )



@endpoints.route('/rest-datasets/gee', methods=['POST'])
def register_dataset():
    """Register GEE Dataset Endpoint"""
    logging.info('Registering new GEE Dataset')

    # Build query
    table_name = request.get_json().get('connector').get('table_name')
    sql = 'SELECT * FROM ' + table_name + ' LIMIT 1'

    # Convert query
    query = QueryService.convert(sql, type='sql')

    try:
        response = EarthEngineService.query(query)
    except GEEQueryError as error:
        logging.error(error.message)
        response = ErrorResponder.build({'status': 500, 'message': error.message})
        return jsonify(response), 500

    config = {
        'uri': '/dataset/'+request.get_json().get('connector').get('id'),
        'method': 'PATCH',
        'body': {'status': 1}
    }
    response = request_to_microservice(config)
    return jsonify(response), 200
