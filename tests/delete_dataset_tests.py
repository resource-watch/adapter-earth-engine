import json
import os

import pytest
import requests_mock

import adapterearthengine

USERS = {
    "ADMIN": {
        "id": '1a10d7c6e0a37126611fd7a7',
        "role": 'ADMIN',
        "provider": 'local',
        "email": 'user@control-tower.org',
        "name": 'John Admin',
        "extraUserData": {
            "apps": [
                'rw',
                'gfw',
                'gfw-climate',
                'prep',
                'aqueduct',
                'forest-atlas',
                'data4sdgs'
            ]
        }
    },
    "MANAGER": {
        "id": '1a10d7c6e0a37126611fd7a7',
        "role": 'MANAGER',
        "provider": 'local',
        "email": 'user@control-tower.org',
        "extraUserData": {
            "apps": [
                'rw',
                'gfw',
                'gfw-climate',
                'prep',
                'aqueduct',
                'forest-atlas',
                'data4sdgs'
            ]
        }
    },
    "USER": {
        "id": '1a10d7c6e0a37126611fd7a7',
        "role": 'USER',
        "provider": 'local',
        "email": 'user@control-tower.org',
        "extraUserData": {
            "apps": [
                'rw',
                'gfw',
                'gfw-climate',
                'prep',
                'aqueduct',
                'forest-atlas',
                'data4sdgs'
            ]
        }
    },
    "MICROSERVICE": {
        "id": "microservice",
        "createdAt": "2016-09-14"
    }
}


@pytest.fixture
def client():
    app = adapterearthengine.app
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


@requests_mock.Mocker(kw='mocker')
def test_delete_dataset_as_microservice(client, mocker):
    get_user_data_calls = mocker.get(os.getenv('CT_URL') + '/auth/user/me', status_code=200, json=USERS['MICROSERVICE'])

    response = client.delete(
        '/api/v1/earthengine/rest-datasets/gee/:dataset', headers={'Authorization': 'Bearer abcd'})
    assert response.data == b''
    assert response.status_code == 204
    assert get_user_data_calls.called
    assert get_user_data_calls.call_count == 1


@requests_mock.Mocker(kw='mocker')
def test_delete_dataset_as_admin(client, mocker):
    get_user_data_calls = mocker.get(os.getenv('CT_URL') + '/auth/user/me', status_code=200, json=USERS['ADMIN'])

    response = client.delete(
        '/api/v1/earthengine/rest-datasets/gee/:dataset', headers={'Authorization': 'Bearer abcd'})
    assert response.data == b''
    assert response.status_code == 204
    assert get_user_data_calls.called
    assert get_user_data_calls.call_count == 1


@requests_mock.Mocker(kw='mocker')
def test_delete_dataset_as_manager(client, mocker):
    get_user_data_calls = mocker.get(os.getenv('CT_URL') + '/auth/user/me', status_code=200, json=USERS['MANAGER'])

    response = client.delete(
        '/api/v1/earthengine/rest-datasets/gee/:dataset', headers={'Authorization': 'Bearer abcd'})
    assert json.loads(response.data) == {'errors': [{'detail': 'Not authorized', 'status': 403}]}
    assert response.status_code == 403
    assert get_user_data_calls.called
    assert get_user_data_calls.call_count == 1
