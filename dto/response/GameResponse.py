from dto.response.BaseResponse import BaseResponse

class GameResponse(BaseResponse):
    def __init__(self, game_id):
        super().__init__()
        self.game_id = game_id

    def to_dict(self):
        d = super().to_dict()
        d["gameId"] = self.game_id
        return d