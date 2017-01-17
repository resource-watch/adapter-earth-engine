import os
import logging

from flask import jsonify, request
import requests

from . import endpoints
from adapterearthengine.responders import ErrorResponder, DatasetResponder
from adapterearthengine.schemas import DatasetSchema
from adapterearthengine.services import EarthEngineService, QueryService
from adapterearthengine.errors import SqlFormatError, GEEQueryError
from adapterearthengine.utils import http

@endpoints.route('/query/<dataset_id>', methods=['POST'])
def query(dataset_id):
    """Query Endpoint"""
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
        return jsonify(response), 500
    except GEEQueryError as error:
        logging.error(error.message)
        response = ErrorResponder.build({'status': 500, 'message': error.message})
        return jsonify(response), 500
    else:
        logging.error(error.message)
        response = ErrorResponder.build({'status': 500, 'message': 'Generic Error'})
        return jsonify(response), 500

    return jsonify(response), 200


@endpoints.route('/fields/<dataset>', methods=['POST'])
def fields():
  return jsonify({'data': 'not yet'}), 200


@endpoints.route('/download/<dataset>', methods=['POST'])
def download():
  return jsonify({'data': 'not yet'}), 200


@endpoints.route('/rest-datasets/gee', methods=['POST'])
def register_dataset():
  """Register Dataset Endpoint"""
  logging.info('Registering new GEE Dataset')

  # Get and deserialize
  dataset = DatasetResponder().deserialize(request.get_json())

  # Build query
  table_name = dataset.get('tableName')
  sql = 'SELECT count(*) FROM ' + table_name + ' LIMIT 1'

  # Get data
  query = QueryService.convert(sql, type='sql')
  response = EarthEngineService.query(query)

  if response:
      config = {
          'uri': '/dataset/'+dataset.get('id', None),
          'method': 'PATCH',
          'body': {'status': 'saved'}
      }
      response = request_to_microservice(config)
      # @TODO
      return jsonify({'data': 'not yet'}), 200
  else:
      response = ErrorResponder.build({'status': 404, 'message': 'Resource Not Found'})
      return jsonify(response), 404
