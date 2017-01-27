from hyp.marshmallow import Responder
from adapterearthengine.schemas import ErrorSchema, DatasetSchema, QuerySchema, FieldsSchema


class ErrorResponder(Responder):
    TYPE = 'errors'
    SERIALIZER = ErrorSchema


class DatasetResponder(Responder):
    TYPE = 'data'
    SERIALIZER = DatasetSchema

    def deserialize(self, dataset, from_filter=True):
        if from_filter:
            dataset = dataset.get('dataset', {})
        dataset = dataset.get(self.TYPE)
        dataset = self.SERIALIZER().dump(dataset).data
        return dataset


class QueryResponder(Responder):
    TYPE = 'data'
    SERIALIZER = QuerySchema

    def deserialize(self, query):
        query = query.get(self.TYPE)
        query = self.SERIALIZER().dump(query).data
        return query

    def serialize(self, features):
        result = features

        def get_values(feature):
            for key, value in feature.get('properties').iteritems():
                feature[key] = value

            feature['the_geom'] = feature['geometry']
            del feature['type']
            del feature['properties']
            del feature['geometry']
            return feature

        if len(result) and 'properties' in result[0]:
            result = map(get_values, result)

        return result


class FieldsResponder(Responder):
    TYPE = 'data'
    SERIALIZER = FieldsSchema

    def serialize(self, fields):
        result = {}
        for key, value in fields.iteritems():
            result[key] = {}
            result[key]['type'] = value

        return result
