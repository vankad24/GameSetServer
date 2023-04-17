from flask import request

class GameRequest:
    def __init__(self, token, game_id):
        self.game_id = game_id
        self.token = token

    @staticmethod
    def from_request():
        data = request.get_json()
        return GameRequest(
            data.get('accessToken',''),
            data.get('gameId',''),
        )

