class ApiException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.msg = message