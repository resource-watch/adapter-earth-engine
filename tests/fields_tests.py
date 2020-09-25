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
def test_get_fields_for_dataset_that_does_not_exist(client, mocker):
    mocker.get('http://test.com/v1/dataset/foo', status_code=404,
               json={"errors": [{"status": 404, "detail": "Dataset with id 'foo' doesn't exist"}]})

    response = client.post('/api/v1/earthengine/fields/foo')
    assert response.status_code == 404
    assert response.data == b'{"errors":[{"detail":"Dataset with id foo doesn\'t exist","status":404}]}\n'


@requests_mock.Mocker(kw='mocker')
def test_get_fields_for_dataset_invalid_provider(client, mocker):
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

    response = client.post('/api/v1/earthengine/fields/bar')
    assert response.status_code == 422
    assert response.data == b'{"errors":[{"detail":"This operation is only supported for datasets with provider \'gee\'","status":422}]}\n'


@requests_mock.Mocker(kw='mocker')
def test_get_fields_for_dataset_invalid_connector_type(client, mocker):
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

    response = client.post('/api/v1/earthengine/fields/bar')
    assert response.status_code == 422
    assert response.data == b'{"errors":[{"detail":"This operation is only supported for datasets with connectorType \'rest\'","status":422}]}\n'


@requests_mock.Mocker(kw='mocker')
def test_get_fields_for_dataset_happy_case(client, mocker):
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

    query_json = {
        "data": {
            "type": "result",
            "attributes": {
                "query": "SELECT * FROM \"srtm90_v4\" LIMIT 1",
                "jsonSql": {
                    "select": [
                        {
                            "value": "*",
                            "alias": None,
                            "type": "wildcard"
                        }
                    ],
                    "from": "srtm90_v4",
                    "limit": 1
                }
            }
        }
    }

    mocker.get('http://test.com/v1/dataset/bar', json=dataset_json)

    mocker.get('http://test.com/v1/convert/sql2SQL?sql=SELECT%20*%20FROM%20%22srtm90_v4%22%20LIMIT%201',
               json=query_json)

    response = client.post('/api/v1/earthengine/fields/bar')
    assert response.status_code == 200
    assert response.data == b'{"data":{"fields":{"bands":[{"dataType":{"precision":"INT","range":{"max":32767,"min":-32768}},"grid":{"affineTransform":{"scaleX":0.000833333333333,"scaleY":-0.000833333333333,"translateX":-180,"translateY":60},"crsCode":"EPSG:4326","dimensions":{"height":144000,"width":432000}},"id":"elevation","pyramidingPolicy":"MEAN"}],"endTime":"2000-02-22T00:00:00Z","geometry":{"coordinates":[[[-180,-59.999999999951996],[179.99999999985602,-59.999999999951996],[179.99999999985602,60],[-180,60],[-180,-59.999999999951996]]],"type":"Polygon"},"id":"srtm90_v4","name":"projects/earthengine-public/assets/srtm90_v4","sizeBytes":"18827626666","startTime":"2000-02-11T00:00:00Z","type":"IMAGE","updateTime":"2017-05-08T19:32:14.303Z"},"tableName":"srtm90_v4"}}\n'
