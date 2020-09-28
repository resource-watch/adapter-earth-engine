class Error(Exception):

    def __init__(self, message):
        self.message = message


class SqlFormatError(Error):
    pass


class GEEQueryError(Error):
    pass


class GeojsonNotFound(Error):
    pass


class DatasetNotFound(Error):
    pass
