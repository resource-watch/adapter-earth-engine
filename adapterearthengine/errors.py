

class Error(Exception):

    def __init__(self, name, message):
        self.name = name
        self.message = message


class SqlFormatError(Error):

    def __init__(self, message):
        Error.__init__(self,
         name='SqlFormatError',
         message=message
     )


class GEEQueryError(Error):

    def __init__(self, message):
        Error.__init__(self,
         name='GEEQueryError',
         message=message
     )
