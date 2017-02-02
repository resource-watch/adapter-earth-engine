import os
import json
import csv
import StringIO
import logging

from flask import jsonify, request, Response, stream_with_context
import requests

from . import endpoints
from adapterearthengine.responders import ErrorResponder, DatasetResponder, QueryResponder, FieldsResponder
from adapterearthengine.services import EarthEngineService, QueryService
from adapterearthengine.errors import SqlFormatError, GEEQueryError, GeojsonNotFound
from adapterearthengine.utils.http import request_to_microservice

@endpoints.route('/query/<dataset_id>', methods=['POST'])
def query(dataset_id):
    """Query GEE Dataset Endpoint"""
    logging.info('Doing GEE Query')

    # Get and deserialize
    dataset = DatasetResponder().deserialize(request.get_json())
    table_type = QueryService.get_type(dataset.get('attributes').get('tableName'))

    sql = request.args.get('sql', None) or request.get_json().get('sql', None)
    fs = request.args.get('fs', None) or request.get_json().get('fs', None)

    if not sql and not fs:
        response = ErrorResponder.build({
            'status': 400,
            'message': 'sql or fs param is required'
        })
        return jsonify(response), 400

    # geostore
    geostore = request.args.get('geostore', None) or request.get_json().get('geostore', None)
    if geostore and sql:
        sql = sql+'&geostore='+geostore
    if geostore and fs:
        fs = fs+'&geostore='+geostore

    # convert
    try:
        if fs:
            query, json_sql = QueryService.convert(fs, type='fs')
        else:
            query, json_sql = QueryService.convert(sql, type='sql')
    except SqlFormatError as error:
        logging.error(error.message)
        response = ErrorResponder.build({'status': 400, 'message': error.message})
        return jsonify(response), 400
    except Exception as error:
        response = ErrorResponder.build({'status': 500, 'message': 'Generic Error'})
        return jsonify(response), 500

    # geojson
    geojson = None
    try:
        if query.index('ST_INTERSECTS'):
            geojson = QueryService.get_geojson(json_sql)
    except:
        pass

    # query
    try:
        response = EarthEngineService.query(query, geojson=geojson)
    except GEEQueryError as error:
        logging.error(error.message)
        response = ErrorResponder.build({'status': 500, 'message': error.message})
        return jsonify(response), 500
    except Exception as error:
        response = ErrorResponder.build({'status': 500, 'message': 'Generic Error'})
        return jsonify(response), 500

    if table_type is 'ft':
        if not isinstance(response, dict):
            value = response
            response = {
                'features': [{'FUNCTION': value}]
            }
        features = QueryResponder().serialize(response.get('features', {}))

    def generate_json():
        yield '{"cloneUrl": ' + json.dumps(QueryService.get_clone_url(dataset.get('id'))) + ','
        if table_type is 'ft':
            f_len = len(features)
            yield '"data": ['
            for idx, feature in enumerate(features):
                if idx != f_len-1:
                    yield json.dumps(feature) + ', '
                else:
                    yield json.dumps(feature)
            yield ']}'
        elif table_type is 'raster':
            yield '"data": ['
            yield json.dumps(response)
            yield ']}'

    return Response(stream_with_context(generate_json()),
        mimetype='application/json',
    )


@endpoints.route('/fields/<dataset_id>', methods=['POST'])
def fields(dataset_id):
    """Get GEE Dataset Fields Endpoint"""
    logging.info('Getting fields of a GEE Dataset')

    # Get and deserialize
    dataset = DatasetResponder().deserialize(request.get_json())

    # Build query
    table_name = dataset.get('attributes').get('tableName')
    table_type = QueryService.get_type(dataset.get('attributes').get('tableName'))

    if table_type is 'raster':
        response = FieldsResponder.build({'tableName': table_name, 'fields': []})
        return jsonify(response), 200

    sql = 'SELECT * FROM \"' + table_name + '\" LIMIT 1'

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
    table_type = QueryService.get_type(dataset.get('attributes').get('tableName'))

    sql = request.args.get('sql', None) or request.get_json().get('sql', None)
    fs = request.args.get('fs', None) or request.get_json().get('fs', None)

    if not sql and not fs:
        response = ErrorResponder.build({
            'status': 400,
            'message': 'sql or fs param is required'
        })
        return jsonify(response), 400

    geojson = None
    geostore = request.args.get('geostore', None)
    if geostore:
        geojson = QueryService.get_geojson()

    # Query format and query to GEE
    try:
        if fs:
           query = QueryService.convert(fs, type='fs')
        else:
           query = QueryService.convert(sql, type='sql')
        response = EarthEngineService.query(query, geojson=geojson)
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

    if table_type is 'ft':
        if not isinstance(response, dict):
            value = response
            response = {
                'features': [{'FUNCTION': value}]
            }
        features = QueryResponder().serialize(response.get('features', {}))

    class Row(object):
        def __init__(self):
            self.row = None
        def write(self, row):
            self.row = row
        def read(self):
            return self.row

    def generate_csv():
        row = Row()
        writer = csv.writer(row)
        if table_type is 'ft':
            writer.writerow(features[0].keys())
        elif table_type is 'raster':
            writer.writerow(response.keys())

        yield row.read()

        def encode_feature_values(value):
            if isinstance(value, basestring):
                return value.encode('utf-8')
            else:
                return value

        if table_type is 'ft':
            for feature in features:
                writer.writerow(map(encode_feature_values, feature.values()))
                yield row.read()
        elif table_type is 'raster':
            for key in response.keys():
                writer.writerow([response[key]])
                yield row.read()

    def generate_json():
        if table_type is 'ft':
            f_len = len(features)
            yield '"data": ['
            for idx, feature in enumerate(features):
                if idx != f_len-1:
                    yield json.dumps(feature) + ', '
                else:
                    yield json.dumps(feature)
            yield ']}'
        elif table_type is 'raster':
            k_len = len(response.keys())
            yield '"data": ['
            for idx, key in enumerate(response.keys()):
                if idx != k_len-1:
                    yield json.dumps(response[key]) + ', '
                else:
                    yield json.dumps(response[key])
            yield ']}'

    format = request.args.get('format', None)
    if format == 'csv':
        return Response(stream_with_context(generate_csv()),
            mimetype='text/csv',
            headers={
                'Content-Disposition': 'attachment; filename=export.csv',
                'Content-type': 'text/csv'
            }
        )
    else:
        return Response(stream_with_context(generate_json()),
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
    table_type = QueryService.get_type(table_name=table_name)

    sql = 'SELECT * FROM \"' + table_name + '\" LIMIT 1'

    if table_type is 'raster':
        sql = 'SELECT ST_METADATA() from \"'+table_name+'\"'

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
