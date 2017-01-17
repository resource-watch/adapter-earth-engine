from hyp.marshmallow import Responder
from adapterearthengine.schemas import ErrorSchema, DatasetSchema


class ErrorResponder(Responder):
    TYPE = 'errors'
    SERIALIZER = ErrorSchema


class DatasetResponder(Responder):
    TYPE = 'attributes'
    SERIALIZER = DatasetSchema

    def deserialize(self, dataset):
        dataset = dataset.get('dataset', {}).get('data')
        dataset = self.SERIALIZER(only=[self.TYPE]).dump(dataset)
        return dataset.data.get(self.TYPE)


class QueryResponder(Responder):
    TYPE = 'attributes'
    SERIALIZER = DatasetSchema

    def deserialize(self, query):
        query = query.get('data', {})
        query = self.SERIALIZER(only=[self.TYPE]).dump(query)
        return query.data.get(self.TYPE)
