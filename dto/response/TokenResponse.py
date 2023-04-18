from dto.response.BaseResponse import BaseResponse

class TokenResponse(BaseResponse):
    def __init__(self, token, nick):
        super().__init__()
        self.accessToken = token
        self.nickname = nick

    def to_dict(self):
        d = super().to_dict()
        d["accessToken"] = self.accessToken
        d["nickname"] = self.nickname
        return d