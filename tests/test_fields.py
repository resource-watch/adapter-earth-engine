import os
import requests_mock
from RWAPIMicroservicePython.test_utils import mock_request_validation

from tests.mocks import mock_get_dataset

from tests.fixtures import (
    dataset_invalid_connector_type,
    dataset_invalid_provider,
    dataset_json,
)


@requests_mock.Mocker(kw="mocker")
def test_get_fields_for_dataset_that_does_not_exist(client, mocker):
    json_response = {
        "errors": [{"status": 404, "detail": "Dataset with id 'bar' doesn't exist"}]
    }
    mock_get_dataset(mocker, json_response)
    mock_request_validation(mocker, microservice_token=os.getenv("MICROSERVICE_TOKEN"))

    response = client.get(
        "/api/v1/earthengine/fields/bar", headers={"x-api-key": "api-key-test"}
    )
    assert response.status_code == 404
    assert (
        response.data
        == b'{"errors":[{"detail":"Dataset with id bar doesn\'t exist","status":404}]}\n'
    )


@requests_mock.Mocker(kw="mocker")
def test_get_fields_for_dataset_invalid_provider(client, mocker):
    mock_get_dataset(mocker, dataset_invalid_provider)
    mock_request_validation(mocker, microservice_token=os.getenv("MICROSERVICE_TOKEN"))

    response = client.get(
        "/api/v1/earthengine/fields/bar", headers={"x-api-key": "api-key-test"}
    )
    assert response.status_code == 422
    assert (
        response.data
        == b'{"errors":[{"detail":"This operation is only supported for datasets with provider \'gee\'","status":422}]}\n'
    )


@requests_mock.Mocker(kw="mocker")
def test_get_fields_for_dataset_invalid_connector_type(client, mocker):
    mock_get_dataset(mocker, dataset_invalid_connector_type)
    mock_request_validation(mocker, microservice_token=os.getenv("MICROSERVICE_TOKEN"))

    response = client.get(
        "/api/v1/earthengine/fields/bar", headers={"x-api-key": "api-key-test"}
    )
    assert response.status_code == 422
    assert (
        response.data
        == b'{"errors":[{"detail":"This operation is only supported for datasets with connectorType \'rest\'","status":422}]}\n'
    )


@requests_mock.Mocker(kw="mocker")
def test_get_fields_for_dataset_happy_case(client, mocker):
    query_json = {
        "data": {
            "type": "result",
            "attributes": {
                "query": 'SELECT * FROM "srtm90_v4" LIMIT 1',
                "jsonSql": {
                    "select": [{"value": "*", "alias": None, "type": "wildcard"}],
                    "from": "srtm90_v4",
                    "limit": 1,
                },
            },
        }
    }

    mock_get_dataset(mocker, dataset_json)
    mock_request_validation(mocker, microservice_token=os.getenv("MICROSERVICE_TOKEN"))
    mocker.get(
        f"{os.getenv('GATEWAY_URL')}/v1/convert/sql2SQL?sql=SELECT%20*%20FROM%20%22srtm90_v4%22%20LIMIT%201",
        json=query_json,
    )

    response = client.get(
        "/api/v1/earthengine/fields/bar", headers={"x-api-key": "api-key-test"}
    )
    assert response.status_code == 200
    assert (
        response.data
        == b'{"data":{"fields":{"bands":[{"dataType":{"precision":"INT","range":{"max":32767,"min":-32768}},"grid":{"affineTransform":{"scaleX":0.000833333333333,"scaleY":-0.000833333333333,"translateX":-180,"translateY":60},"crsCode":"EPSG:4326","dimensions":{"height":144000,"width":432000}},"id":"elevation","pyramidingPolicy":"MEAN"}],"endTime":"2000-02-22T00:00:00Z","geometry":{"coordinates":[[[-180,-59.999999999951996],[179.99999999985602,-59.999999999951996],[179.99999999985602,60],[-180,60],[-180,-59.999999999951996]]],"type":"Polygon"},"id":"srtm90_v4","name":"projects/earthengine-public/assets/srtm90_v4","sizeBytes":"18827626666","startTime":"2000-02-11T00:00:00Z","type":"IMAGE","updateTime":"2017-05-08T19:32:14.303Z"},"tableName":"srtm90_v4"}}\n'
    )
