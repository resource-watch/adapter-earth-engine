import pytest
from moto import mock_logs


@pytest.fixture(scope="package")
def client():
    mocked_logs = mock_logs()
    mocked_logs.start()

    from adapterearthengine import app

    app.config["TESTING"] = True
    client = app.test_client()

    yield client
    mocked_logs.stop()
