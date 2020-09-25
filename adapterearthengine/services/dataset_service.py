from CTRegisterMicroserviceFlask import request_to_microservice

from adapterearthengine.errors import DatasetNotFound


class DatasetService(object):

    @staticmethod
    def execute(config):
        response = request_to_microservice(config)
        if not response or response.get('errors'):
            raise DatasetNotFound(message='Dataset not found')
        dataset = response.get('data', None).get('attributes', None)
        return dataset

    @staticmethod
    def get(dataset):
        config = {
            'uri': '/dataset/' + dataset,
            'method': 'GET'
        }
        return DatasetService.execute(config)
