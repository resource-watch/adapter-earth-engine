from RWAPIMicroservicePython import request_to_microservice

from adapterearthengine.errors import DatasetNotFound


class DatasetService(object):
    @staticmethod
    def execute(uri, api_key):
        response = request_to_microservice(uri=uri, api_key=api_key, method="GET")
        if not response or response.get("errors"):
            raise DatasetNotFound(message="Dataset not found")
        dataset = response.get("data", None).get("attributes", None)
        return dataset

    @staticmethod
    def get(dataset, api_key):
        uri = f"/v1/dataset/{dataset}"
        return DatasetService.execute(uri, api_key)
