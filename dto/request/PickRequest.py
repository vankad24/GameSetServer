from flask import request

class PickRequest:
    def __init__(self, token, cards_ids):
        self.cards_ids = cards_ids
        self.token = token

    @staticmethod
    def from_request():
        data = request.get_json()
        return PickRequest(
            data.get('accessToken',''),
            data.get('cards',[]),
        )

