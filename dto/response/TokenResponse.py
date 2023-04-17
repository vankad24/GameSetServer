from dto.response.BaseResponse import BaseResponse
from model.User import User


class TokenResponse(BaseResponse):
    def __init__(self, nick, token):
        super().__init__()
        self.accessToken = token
        self.nickname = nick

    def to_dict(self):
        d = super().to_dict()
        d["accessToken"] = self.accessToken
        d["nickname"] = self.nickname
        return d