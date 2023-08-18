import os
import json
import requests_mock
from RWAPIMicroservicePython.test_utils import mock_request_validation

from tests.mocks import mock_get_dataset, mock_convert_sql
from tests.fixtures import (
    dataset_invalid_connector_type,
    dataset_json,
    dataset_invalid_provider,
    query_json,
)


@requests_mock.Mocker(kw="mocker")
def test_query_dataset_that_does_not_exist(client, mocker):
    json_response = {
        "errors": [{"status": 404, "detail": "Dataset with id 'bar' doesn't exist"}]
    }

    mock_get_dataset(mocker, json_response)
    mock_request_validation(mocker, microservice_token=os.getenv("MICROSERVICE_TOKEN"))

    response = client.post(
        "/api/v1/earthengine/query/bar", headers={"x-api-key": "api-key-test"}
    )
    assert response.status_code == 404
    assert (
        response.data
        == b'{"errors":[{"detail":"Dataset with id bar doesn\'t exist","status":404}]}\n'
    )


@requests_mock.Mocker(kw="mocker")
def test_query_dataset_invalid_provider(client, mocker):
    mock_get_dataset(mocker, dataset_invalid_provider)
    mock_request_validation(mocker, microservice_token=os.getenv("MICROSERVICE_TOKEN"))

    response = client.post(
        "/api/v1/earthengine/query/bar", headers={"x-api-key": "api-key-test"}
    )
    assert response.status_code == 422
    assert (
        response.data
        == b'{"errors":[{"detail":"This operation is only supported for datasets with provider \'gee\'","status":422}]}\n'
    )


@requests_mock.Mocker(kw="mocker")
def test_query_dataset_invalid_connector_type(client, mocker):
    mock_get_dataset(mocker, dataset_invalid_connector_type)
    mock_request_validation(mocker, microservice_token=os.getenv("MICROSERVICE_TOKEN"))

    response = client.post(
        "/api/v1/earthengine/query/bar", headers={"x-api-key": "api-key-test"}
    )
    assert response.status_code == 422
    assert (
        response.data
        == b'{"errors":[{"detail":"This operation is only supported for datasets with connectorType \'rest\'","status":422}]}\n'
    )


@requests_mock.Mocker(kw="mocker")
def test_query_dataset_no_query(client, mocker):
    mock_get_dataset(mocker, dataset_json)
    mock_request_validation(mocker, microservice_token=os.getenv("MICROSERVICE_TOKEN"))

    response = client.post(
        "/api/v1/earthengine/query/bar", headers={"x-api-key": "api-key-test"}, json={}
    )
    assert response.status_code == 400
    assert (
        response.data
        == b'{"errors":[{"detail":"sql or fs not provided","status":400}]}\n'
    )


# Failing because of an issue with sql2gee
@requests_mock.Mocker(kw="mocker")
def test_query_dataset_happy_case(client, mocker):
    mock_get_dataset(mocker, dataset_json)
    mock_convert_sql(mocker, query_json)
    mock_request_validation(mocker, microservice_token=os.getenv("MICROSERVICE_TOKEN"))

    response = client.post(
        "/api/v1/earthengine/query/bar",
        headers={"x-api-key": "api-key-test"},
        json={
            "sql": "SELECT%20ST_HISTOGRAM%28rast%2C%20elevation%2C%2010%2C%20true%29%20FROM%20CGIAR%2FSRTM90_V4"
        },
    )

    assert response.status_code == 200

    json_response = json.loads(response.data)
    assert "data" in json_response
    assert "st_histogram" in json_response["data"][0]
    assert "elevation" in json_response["data"][0]["st_histogram"]
    assert len(json_response["data"][0]["st_histogram"]["elevation"]) == 10
