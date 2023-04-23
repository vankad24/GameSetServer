from dto.response.GameResponse import GameResponse


class CreateGameStatisticsResponse(GameResponse):
    def __init__(self, score, game):
        super().__init__(score, game)
        self.statistics = game.scores

    def to_dict(self):
        d = super().to_dict()
        arr = []
        for uid, score in self.statistics.items():
            arr.append({"id":uid,"score":score})
        d["stats"] = arr
        return d