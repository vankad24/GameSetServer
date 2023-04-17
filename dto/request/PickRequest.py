from flask import request

class PickRequest:
    def __init__(self, token, cards):
        self.cards = cards
        self.token = token

    @staticmethod
    def from_request():
        data = request.get_json()
        return PickRequest(
            data.get('accessToken',''),
            data.get('cards',[]),
        )

