from dto.response.GameResponse import GameResponse


class PickResponse(GameResponse):
    def __init__(self, is_set, score, game):
        super().__init__(score, game)
        self.is_set = is_set

    def to_dict(self):
        d = super().to_dict()
        d["isSet"] = self.is_set
        return d