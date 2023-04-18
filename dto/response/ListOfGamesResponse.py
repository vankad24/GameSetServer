from dto.response.BaseResponse import BaseResponse

class ListOfGamesResponse(BaseResponse):
    def __init__(self, ids):
        super().__init__()
        self.ids = ids

    def to_dict(self):
        d = super().to_dict()
        arr = []
        for game_id in self.ids:
            arr.append({"id":game_id})
        d["games"] = arr
        return d