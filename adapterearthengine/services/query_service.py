import logging
from flask import request

from RWAPIMicroservicePython import request_to_microservice

from adapterearthengine.errors import SqlFormatError


def convert(query, query_type="sql"):
    if not query:
        raise SqlFormatError(message="sql or fs not provided")
    if query_type == "fs" and "&" not in query:
        raise SqlFormatError(message="sql or fs not provided")

    logging.info("Converting Query: " + query)

    endpoint = "sql2SQL"
    if query_type == "fs":
        endpoint = "fs2SQL"

    result = endpoint + query
    logging.info(f"[QUERY SERVICE - convert]: {result}")

    try:
        response = request_to_microservice(
            uri=f"/v1/convert/{result}",
            method="GET",
            api_key=request.headers.get("x-api-key"),
        )
        return response
    except Exception as error:
        raise error

    if response.get("errors"):
        errors = response.get("errors")
        raise SqlFormatError(message=errors[0].get("detail"))


def get_geojson(geostore):
    try:
        response = request_to_microservice(
            uri=f"/v1/geostore/{geostore}",
            method="GET",
            api_key=request.headers.get("x-api-key"),
        )
        return response.get("data").get("attributes").get("geojson")
    except Exception as error:
        raise error

    if response.get("errors"):
        errors = response.get("errors")
        raise SqlFormatError(message=errors[0].get("detail"))


def get_type(table_name):
    logging.info("Getting Dataset Type")

    if "ft:" in table_name:
        return "ft"
    else:
        return "raster"


def get_clone_url(dataset_id, query):
    return {
        "httpMethod": "POST",
        "url": "/v1/dataset/" + dataset_id + "/clone",
        "body": {
            "dataset": {
                "datasetUrl": "/query/" + dataset_id + "?sql=" + query,
                "application": ["your", "apps"],
            }
        },
    }
