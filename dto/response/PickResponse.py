from dto.response.BaseResponse import BaseResponse

class PickResponse(BaseResponse):
    def __init__(self, is_set, score):
        super().__init__()
        self.score = score
        self.is_set = is_set

    def to_dict(self):
        d = super().to_dict()
        d["isSet"] = self.is_set
        d["score"] = self.score
        return d