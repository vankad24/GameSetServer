from flask import request

class BaseRequest:
    def __init__(self, token):
        self.token = token

    @staticmethod
    def from_request():
        data = request.get_json()
        return BaseRequest(
            data.get('accessToken',''),
        )

