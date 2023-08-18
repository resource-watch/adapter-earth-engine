import json
import os

import requests_mock
from RWAPIMicroservicePython.test_utils import mock_request_validation

from tests.fixtures import USERS


@requests_mock.Mocker(kw="mocker")
def test_delete_dataset_as_microservice(client, mocker):
    get_user_data_calls = mock_request_validation(
        mocker,
        microservice_token=os.getenv("MICROSERVICE_TOKEN"),
        user=USERS["MICROSERVICE"],
    )

    response = client.delete(
        "/api/v1/earthengine/rest-datasets/gee/:dataset",
        headers={"Authorization": "Bearer abcd", "x-api-key": "api-key-test"},
    )
    assert response.data == b""
    assert response.status_code == 204
    assert get_user_data_calls.called
    assert get_user_data_calls.call_count == 1


@requests_mock.Mocker(kw="mocker")
def test_delete_dataset_as_admin(client, mocker):
    get_user_data_calls = mock_request_validation(
        mocker, microservice_token=os.getenv("MICROSERVICE_TOKEN"), user=USERS["ADMIN"]
    )

    response = client.delete(
        "/api/v1/earthengine/rest-datasets/gee/:dataset",
        headers={"Authorization": "Bearer abcd", "x-api-key": "api-key-test"},
    )
    assert response.data == b""
    assert response.status_code == 204
    assert get_user_data_calls.called
    assert get_user_data_calls.call_count == 1


@requests_mock.Mocker(kw="mocker")
def test_delete_dataset_as_manager(client, mocker):
    get_user_data_calls = mock_request_validation(
        mocker,
        microservice_token=os.getenv("MICROSERVICE_TOKEN"),
        user=USERS["MANAGER"],
    )

    response = client.delete(
        "/api/v1/earthengine/rest-datasets/gee/:dataset",
        headers={"Authorization": "Bearer abcd", "x-api-key": "api-key-test"},
    )
    assert json.loads(response.data) == {
        "errors": [{"detail": "Not authorized", "status": 403}]
    }
    assert response.status_code == 403
    assert get_user_data_calls.called
    assert get_user_data_calls.call_count == 1
