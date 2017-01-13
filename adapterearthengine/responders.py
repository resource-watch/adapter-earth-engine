from hyp.marshmallow import Responder
from adapterearthengine.schemas import ErrorSchema


class ErrorResponder(Responder):
    TYPE = 'errors'
    SERIALIZER = ErrorSchema
