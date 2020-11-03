"""Serializers"""


def serialize_query(data, meta):
    """."""
    return {
        'data': data,
        'meta': meta
    }


def serialize_fields(fields, table_name):
    """."""
    return {
        'tableName': table_name,
        'fields': fields
    }
