import json

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
    response = client.delete(
        '/api/v1/earthengine/rest-datasets/gee/:dataset?loggedUser={}'.format(json.dumps(USERS['MICROSERVICE'])))
    assert response.data == b''
    assert response.status_code == 204


@requests_mock.Mocker(kw='mocker')
def test_delete_dataset_as_admin(client, mocker):
    response = client.delete(
        '/api/v1/earthengine/rest-datasets/gee/:dataset?loggedUser={}'.format(json.dumps(USERS['ADMIN'])))
    assert response.data == b''
    assert response.status_code == 204


@requests_mock.Mocker(kw='mocker')
def test_delete_dataset_as_manager(client, mocker):
    response = client.delete(
        '/api/v1/earthengine/rest-datasets/gee/:dataset?loggedUser={}'.format(json.dumps(USERS['MANAGER'])))
    assert json.loads(response.data) == {'errors': [{'detail': 'Not authorized', 'status': 403}]}
    assert response.status_code == 403
