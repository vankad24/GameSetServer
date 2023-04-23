from dto.response.GameRoomResponse import GameRoomResponse
from model.Game import Game


class GameResponse(GameRoomResponse):
    def __init__(self, score, game: Game):
        super().__init__(game)
        self.score = score

    def to_dict(self):
        d = super().to_dict()
        d["score"] = self.score
        return d