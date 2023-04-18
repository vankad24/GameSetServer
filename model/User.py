class User:
    def __init__(self, uid:int, nickname: str, password: str, token: str):
        self.id = uid
        self.token = token
        self.password = password
        self.nickname = nickname