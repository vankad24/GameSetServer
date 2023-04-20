from dto.response.BaseResponse import BaseResponse

class FindSetResponse(BaseResponse):
    def __init__(self, ids, score):
        super().__init__()
        self.score = score
        self.ids = ids

    def to_dict(self):
        d = super().to_dict()
        d["cards"] = self.ids
        d["score"] = self.score
        return d