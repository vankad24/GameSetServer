from dto.response.BaseResponse import BaseResponse

class GameStatisticsResponse(BaseResponse):
    def __init__(self, statistics):
        super().__init__()
        self.statistics = statistics

    def to_dict(self):
        d = super().to_dict()
        arr = []
        for uid, score in self.statistics.items():
            arr.append({"id":uid,"score":score})
        d["stats"] = arr
        return d