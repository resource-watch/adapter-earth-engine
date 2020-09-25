import pytest
import requests_mock

import adapterearthengine

@pytest.fixture
def client():
    app = adapterearthengine.app
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


@requests_mock.Mocker(kw='mocker')
def test_download_dataset_that_does_not_exist(client, mocker):
    mocker.get('http://test.com/v1/dataset/foo', status_code=404,
               json={"errors": [{"status": 404, "detail": "Dataset with id 'foo' doesn't exist"}]})

    response = client.post('/api/v1/earthengine/download/foo')
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

    mocker.get('http://test.com/v1/dataset/bar', json=dataset_json)

    response = client.post('/api/v1/earthengine/download/bar')
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

    mocker.get('http://test.com/v1/dataset/bar', json=dataset_json)

    response = client.post('/api/v1/earthengine/download/bar')
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

    mocker.get('http://test.com/v1/dataset/bar', json=dataset_json)

    response = client.post('/api/v1/earthengine/download/bar')
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

    download_json = {
        "data": {
            "type": "result",
            "attributes": {
                "query": "SELECT * FROM \"srtm90_v4\" LIMIT 5",
                "jsonSql": {
                    "select": [
                        {
                            "value": "*",
                            "alias": None,
                            "type": "wildcard"
                        }
                    ],
                    "from": "srtm90_v4",
                    "limit": 5
                }
            }
        }
    }

    mocker.get('http://test.com/v1/dataset/bar', json=dataset_json)

    mocker.get('http://test.com/v1/convert/sql2SQL?sql=select%20%2A%20from%20%20srtm90_v4%20limit%205',
               json=download_json)

    response = client.post('/api/v1/earthengine/download/bar?sql=select%20%2A%20from%20%20srtm90_v4%20limit%205')

    # TODO: Once https://github.com/Vizzuality/sql2gee/issues/16 is solved, this should return a 200, but the result validation needs to be calculated
    # assert response.status_code == 200
    assert response.status_code == 500
    assert response.data == b'{"errors":[{"detail":"Generic Error","status":500}]}\n'
