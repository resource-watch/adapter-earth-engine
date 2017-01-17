from marshmallow import Schema, fields


class ErrorSchema(Schema):
    status = fields.Integer()
    message = fields.Str()


class DatasetSchema(Schema):
    id = fields.Str()
    type = fields.Str()
    attributes = fields.Dict()


class QuerySchema(Schema):
    id = fields.Str()
    type = fields.Str()
    attributes = fields.Dict()
    result = fields.Integer()
