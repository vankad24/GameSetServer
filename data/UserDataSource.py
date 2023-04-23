from model.User import User
from uuid import uuid4

class UserDataSource:
    def __init__(self):
        self.data = {}
        with open("users.csv") as f:
            f.readline()
            for line in f:
                line = line.strip(" \t\n")
                if line != "":
                    t = line.split(",")
                    uid = int(t[0])
                    nick = t[1]
                    password = t[2]
                    token = t[3]
                    self.data[token] = User(uid,nick,password,token)

    def get_by_nick(self, nick):
        users = list(filter(lambda u: u.nickname==nick, self.data.values()))
        if len(users)==1:
            return users[0]
        else:
            return None

    def get_by_id(self, uid):
        users = list(filter(lambda u: u.id == uid, self.data.values()))
        if len(users)==1:
            return users[0]
        else:
            return None

    def get_by_token(self, token):
        if token in self.data:
            return self.data[token]
        else:
            return None

    def create_user(self, nickname, password):
        while True:
            new_id = uuid4().int % 1000000
            if self.get_by_id(new_id) is None:
                break
        token = self.generate_token()
        new_user = User(new_id,nickname,password,token)
        self.data[token] = new_user
        with open("users.csv", "a") as f:
            f.write(f"{new_user.id},{new_user.nickname},{new_user.password},{new_user.token}\n")
        return new_user

    def generate_token(self):
        while True:
            new_token = uuid4().hex
            if self.get_by_token(new_token) is None:
                break
        return new_token

    #update in bd
    def update_user(self, uid):
        for token, user in self.data.items():
            with open("users.csv", "w") as f:
                f.write(f"{user.id},{user.nickname},{user.password},{user.token}\n")