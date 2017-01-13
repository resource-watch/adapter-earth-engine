import os
import logging

from flask import jsonify
import requests

from . import endpoints
from adapterearthengine.responders import ErrorResponder
from adapterearthengine.services import EarthEngineService
from adapterearthengine.errors import Error, NotFoundError

# @TODO
def request_to_microservice(config):
    try:
        return requests.get(config.get('uri'))
    except Exception as e:
        raise e


@endpoints.route('/query/<dataset>', methods=['POST'])
def query(dataset):
    """Query Endpoint"""
    logging.info('Doing GEE Query')
    try:
        pass
        # request_to_microservice(dataset) @TODO
    except Exception as e:
        error = {'status': 400, 'detail': ''}

    status = EarthEngineService.query()
    error = {'status': 500, 'detail': 'hey there'}
    response = ErrorResponder.build(error)
    return jsonify(response), 500


@endpoints.route('/fields/<dataset>', methods=['POST'])
def fields():
  return "Hello World!"


@endpoints.route('/download/<dataset>', methods=['POST'])
def download():
  return "Hello World!"
