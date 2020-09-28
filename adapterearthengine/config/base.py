from adapterearthengine.utils.files import BASE_DIR

SETTINGS = {
    'logging': {
        'level': 'DEBUG'
    },
    'service': {
        'name': 'Earth Engine Adapter',
        'uri': 'http://mymachine:5700',
        'port': 5700
    },
    'gee': {
        'service_account': '390573081381-lm51tabsc8q8b33ik497hc66qcmbj11d@developer.gserviceaccount.com',
        'privatekey_file': BASE_DIR + '/privatekey.json'
    }
}
