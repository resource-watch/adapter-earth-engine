import pytest

import adapterearthengine


@pytest.fixture
def client():
    app = adapterearthengine.app
    app.config["TESTING"] = True
    client = app.test_client()

    yield client
