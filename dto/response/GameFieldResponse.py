from dto.response.BaseResponse import BaseResponse

class GameFieldResponse(BaseResponse):
    def __init__(self, field, score):
        super().__init__()
        self.score = score
        self.field = field

    def to_dict(self):
        d = super().to_dict()
        arr = []
        for card in self.field:
            arr.append(card.to_dict())
        d["cards"] = arr
        d["score"] = self.score
        return d