import copy


dataset_json = {
    "data": {
        "id": "bar",
        "type": "dataset",
        "attributes": {
            "name": "Test dataset 1",
            "slug": "test-dataset-1",
            "type": "tabular",
            "subtitle": None,
            "application": ["rw"],
            "dataPath": None,
            "attributesPath": None,
            "connectorType": "rest",
            "provider": "gee",
            "userId": "1",
            "connectorUrl": "https://raw.githubusercontent.com/test/file.csv",
            "sources": [],
            "tableName": "srtm90_v4",
            "status": "saved",
            "published": False,
            "overwrite": True,
            "mainDateField": None,
            "env": "production",
            "geoInfo": False,
            "protected": False,
            "clonedHost": {},
            "legend": {},
            "errorMessage": None,
            "taskId": None,
            "createdAt": "2016-08-01T15:28:15.050Z",
            "updatedAt": "2018-01-05T18:15:23.266Z",
            "dataLastUpdated": None,
            "widgetRelevantProps": [],
            "layerRelevantProps": [],
        },
    }
}

dataset_invalid_provider = copy.deepcopy(dataset_json)
dataset_invalid_provider["data"]["attributes"].update(provider="csv")

dataset_invalid_connector_type = copy.deepcopy(dataset_json)
dataset_invalid_connector_type["data"]["attributes"].update(connectorType="document")

query_json = {
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
                            {"value": "rast", "type": "literal"},
                            {"value": "elevation", "type": "literal"},
                            {"value": 10, "type": "number"},
                            {"value": "true", "type": "literal"},
                        ],
                    }
                ],
                "from": "CGIAR/SRTM90_V4",
            },
        },
    }
}

USERS = {
    "ADMIN": {
        "id": "1a10d7c6e0a37126611fd7a7",
        "role": "ADMIN",
        "provider": "local",
        "email": "user@control-tower.org",
        "name": "John Admin",
        "extraUserData": {
            "apps": [
                "rw",
                "gfw",
                "gfw-climate",
                "prep",
                "aqueduct",
                "forest-atlas",
                "data4sdgs",
            ]
        },
    },
    "MANAGER": {
        "id": "1a10d7c6e0a37126611fd7a7",
        "role": "MANAGER",
        "name": "John Manager",
        "provider": "local",
        "email": "user@control-tower.org",
        "extraUserData": {
            "apps": [
                "rw",
                "gfw",
                "gfw-climate",
                "prep",
                "aqueduct",
                "forest-atlas",
                "data4sdgs",
            ]
        },
    },
    "USER": {
        "id": "1a10d7c6e0a37126611fd7a7",
        "role": "USER",
        "name": "John User",
        "provider": "local",
        "email": "user@control-tower.org",
        "extraUserData": {
            "apps": [
                "rw",
                "gfw",
                "gfw-climate",
                "prep",
                "aqueduct",
                "forest-atlas",
                "data4sdgs",
            ]
        },
    },
    "MICROSERVICE": {"id": "microservice", "createdAt": "2016-09-14"},
}
