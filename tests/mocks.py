import os


def mock_get_dataset(mocker, response_json):
    mocker.get(
        f"{os.getenv('GATEWAY_URL')}/v1/dataset/bar",
        request_headers={
            "content-type": "application/json",
            "x-api-key": "api-key-test",
        },
        status_code=404,
        json=response_json,
    )


def mock_convert_sql(mocker, response_json):
    mocker.get(
        f"{os.getenv('GATEWAY_URL')}/v1/convert/sql2SQL?sql=SELECT%20ST_HISTOGRAM%28rast%2C%20elevation%2C%2010%2C%20true%29%20FROM%20CGIAR%2FSRTM90_V4",
        request_headers={
            "content-type": "application/json",
            "x-api-key": "api-key-test",
        },
        json=response_json,
    )
