from dto.response.GameResponse import GameResponse


class FindSetResponse(GameResponse):
    def __init__(self, ids, score, game):
        super().__init__(score, game)
        self.ids = ids

    def to_dict(self):
        d = super().to_dict()
        d["cards"] = self.ids
        return d