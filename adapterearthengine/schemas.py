from marshmallow import Schema, fields


class ErrorSchema(Schema):
    status = fields.Integer()
    detail = fields.Str()
