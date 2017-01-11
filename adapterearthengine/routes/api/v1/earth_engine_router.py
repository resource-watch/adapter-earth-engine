import os
import logging
from . import endpoints

@endpoints.route('/', methods=['GET'])
def hello_world():
  """World Endpoint Controller"""
  logging.info('Hey there')
  return "Hello World!"
