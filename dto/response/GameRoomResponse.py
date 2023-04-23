from dto.response.BaseResponse import BaseResponse

class GameRoomResponse(BaseResponse):
    def __init__(self, game):
        super().__init__()
        self.game = game

    def to_dict(self):
        d = super().to_dict()
        return d | self.game.to_dict()