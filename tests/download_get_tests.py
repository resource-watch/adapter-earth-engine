import pytest
import os
import requests_mock
import json

import adapterearthengine


@pytest.fixture
def client():
    app = adapterearthengine.app
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


@requests_mock.Mocker(kw='mocker')
def test_download_dataset_that_does_not_exist(client, mocker):
    mocker.get('{}/v1/dataset/foo'.format(os.getenv('CT_URL')), status_code=404,
               json={"errors": [{"status": 404, "detail": "Dataset with id 'foo' doesn't exist"}]})

    response = client.get('/api/v1/earthengine/download/foo')
    assert response.status_code == 404
    assert response.data == b'{"errors":[{"detail":"Dataset with id foo doesn\'t exist","status":404}]}\n'


@requests_mock.Mocker(kw='mocker')
def test_download_dataset_invalid_provider(client, mocker):
    dataset_json = {
        'data': {
            'id': 'bar',
            'type': 'dataset',
            'attributes': {
                'name': 'Test dataset 1',
                'slug': 'test-dataset-1',
                'type': 'tabular',
                'subtitle': None,
                'application': [
                    'rw'
                ],
                'dataPath': None,
                'attributesPath': None,
                'connectorType': 'rest',
                'provider': 'csv',
                'userId': '1',
                'connectorUrl': 'https://raw.githubusercontent.com/test/file.csv',
                'sources': [],
                'tableName': 'index_d1ced4227cd5480a8904d3410d75bf42_1587619728489',
                'status': 'saved',
                'published': False,
                'overwrite': True,
                'mainDateField': None,
                'env': 'production',
                'geoInfo': False,
                'protected': False,
                'clonedHost': {},
                'legend': {},
                'errorMessage': None,
                'taskId': None,
                'createdAt': '2016-08-01T15:28:15.050Z',
                'updatedAt': '2018-01-05T18:15:23.266Z',
                'dataLastUpdated': None,
                'widgetRelevantProps': [],
                'layerRelevantProps': []
            }
        }}

    mocker.get('{}/v1/dataset/bar'.format(os.getenv('CT_URL')), json=dataset_json)

    response = client.get('/api/v1/earthengine/download/bar')
    assert response.status_code == 422
    assert response.data == b'{"errors":[{"detail":"This operation is only supported for datasets with provider \'gee\'","status":422}]}\n'


@requests_mock.Mocker(kw='mocker')
def test_download_dataset_invalid_connector_type(client, mocker):
    dataset_json = {
        'data': {
            'id': 'bar',
            'type': 'dataset',
            'attributes': {
                'name': 'Test dataset 1',
                'slug': 'test-dataset-1',
                'type': 'tabular',
                'subtitle': None,
                'application': [
                    'rw'
                ],
                'dataPath': None,
                'attributesPath': None,
                'connectorType': 'document',
                'provider': 'gee',
                'userId': '1',
                'connectorUrl': 'https://raw.githubusercontent.com/test/file.csv',
                'sources': [],
                'tableName': 'index_d1ced4227cd5480a8904d3410d75bf42_1587619728489',
                'status': 'saved',
                'published': False,
                'overwrite': True,
                'mainDateField': None,
                'env': 'production',
                'geoInfo': False,
                'protected': False,
                'clonedHost': {},
                'legend': {},
                'errorMessage': None,
                'taskId': None,
                'createdAt': '2016-08-01T15:28:15.050Z',
                'updatedAt': '2018-01-05T18:15:23.266Z',
                'dataLastUpdated': None,
                'widgetRelevantProps': [],
                'layerRelevantProps': []
            }
        }}

    mocker.get('{}/v1/dataset/bar'.format(os.getenv('CT_URL')), json=dataset_json)

    response = client.get('/api/v1/earthengine/download/bar')
    assert response.status_code == 422
    assert response.data == b'{"errors":[{"detail":"This operation is only supported for datasets with connectorType \'rest\'","status":422}]}\n'


@requests_mock.Mocker(kw='mocker')
def test_download_dataset_no_download(client, mocker):
    dataset_json = {
        'data': {
            'id': 'bar',
            'type': 'dataset',
            'attributes': {
                'name': 'Test dataset 1',
                'slug': 'test-dataset-1',
                'type': 'tabular',
                'subtitle': None,
                'application': [
                    'rw'
                ],
                'dataPath': None,
                'attributesPath': None,
                'connectorType': 'rest',
                'provider': 'gee',
                'userId': '1',
                'connectorUrl': 'https://raw.githubusercontent.com/test/file.csv',
                'sources': [],
                'tableName': 'srtm90_v4',
                'status': 'saved',
                'published': False,
                'overwrite': True,
                'mainDateField': None,
                'env': 'production',
                'geoInfo': False,
                'protected': False,
                'clonedHost': {},
                'legend': {},
                'errorMessage': None,
                'taskId': None,
                'createdAt': '2016-08-01T15:28:15.050Z',
                'updatedAt': '2018-01-05T18:15:23.266Z',
                'dataLastUpdated': None,
                'widgetRelevantProps': [],
                'layerRelevantProps': []
            }
        }}

    mocker.get('{}/v1/dataset/bar'.format(os.getenv('CT_URL')), json=dataset_json)

    response = client.get('/api/v1/earthengine/download/bar')
    assert response.status_code == 400
    assert response.data == b'{"errors":[{"detail":"sql or fs not provided","status":400}]}\n'


# Failing because of an issue with sql2gee
@requests_mock.Mocker(kw='mocker')
def test_download_dataset_happy_case(client, mocker):
    dataset_json = {
        'data': {
            'id': 'bar',
            'type': 'dataset',
            'attributes': {
                'name': 'Test dataset 1',
                'slug': 'test-dataset-1',
                'type': 'tabular',
                'subtitle': None,
                'application': [
                    'rw'
                ],
                'dataPath': None,
                'attributesPath': None,
                'connectorType': 'rest',
                'provider': 'gee',
                'userId': '1',
                'connectorUrl': 'https://raw.githubusercontent.com/test/file.csv',
                'sources': [],
                'tableName': 'CGIAR/SRTM90_V4',
                'status': 'saved',
                'published': False,
                'overwrite': True,
                'mainDateField': None,
                'env': 'production',
                'geoInfo': False,
                'protected': False,
                'clonedHost': {},
                'legend': {},
                'errorMessage': None,
                'taskId': None,
                'createdAt': '2016-08-01T15:28:15.050Z',
                'updatedAt': '2018-01-05T18:15:23.266Z',
                'dataLastUpdated': None,
                'widgetRelevantProps': [],
                'layerRelevantProps': []
            }
        }}

    download_json = {
        "data": {
            "type": "result",
            "attributes": {
                "query": "SELECT ST_HISTOGRAM(rast,elevation,10,true) FROM CGIAR/SRTM90_V4",
                "jsonSql": {
                    "select": [
                        {
                            "type": "function",
                            "alias": None,
                            "value": "ST_HISTOGRAM",
                            "arguments": [
                                {
                                    "value": "rast",
                                    "type": "literal"
                                },
                                {
                                    "value": "elevation",
                                    "type": "literal"
                                },
                                {
                                    "value": 10,
                                    "type": "number"
                                },
                                {
                                    "value": "true",
                                    "type": "literal"
                                }
                            ]
                        }
                    ],
                    "from": "CGIAR/SRTM90_V4"
                }
            }
        }
    }

    mocker.get('{}/v1/dataset/bar'.format(os.getenv('CT_URL')), json=dataset_json)

    mocker.get(
        '{}/v1/convert/sql2SQL?sql=SELECT%20ST_HISTOGRAM%28rast%2C%20elevation%2C%2010%2C%20true%29%20FROM%20CGIAR%2FSRTM90_V4'.format(os.getenv('CT_URL')),
        json=download_json)

    response = client.get(
        '/api/v1/earthengine/download/bar?sql=SELECT%20ST_HISTOGRAM%28rast%2C%20elevation%2C%2010%2C%20true%29%20FROM%20CGIAR%2FSRTM90_V4')

    assert response.status_code == 200

    json_response = json.loads(response.data)
    assert "data" in json_response
    assert "data" in json_response['data']
    assert "st_histogram" in json_response['data']['data'][0]
    assert "elevation" in json_response['data']['data'][0]['st_histogram']
    assert len(json_response['data']['data'][0]['st_histogram']['elevation']) == 10
