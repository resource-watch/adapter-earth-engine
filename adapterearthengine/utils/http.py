import os
from requests import Request, Session


CT_URL = os.getenv('CT_URL')


def request_to_microservice(config):
    try:
        session = Session()
        request = Request(
                method=config.get('method'),
                url=CT_URL + config.get('uri'),
                headers={
                    'content-type': 'application/json'
                }
            )
        prepped = session.prepare_request(request)
        if config.get('body'):
            prepped.body = config.get('body')

        response = session.send(prepped)
    except Exception as error:
       raise error

    return response.json()
