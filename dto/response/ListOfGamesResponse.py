from dto.response.BaseResponse import BaseResponse


class ListOfGamesResponse(BaseResponse):
    def __init__(self, games):
        super().__init__()
        self.games = games

    def to_dict(self):
        d = super().to_dict()
        arr = []
        for game in self.games:
            arr.append(game.to_dict())
        d["games"] = arr
        return d