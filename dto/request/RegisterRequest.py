from flask import request

class RegisterRequest:
    def __init__(self, nick, password):
        self.nick = nick
        self.password = password

    @staticmethod
    def from_request():
        data = request.get_json()
        return RegisterRequest(
            data.get('nickname',''),
            data.get('password',''),
        )

