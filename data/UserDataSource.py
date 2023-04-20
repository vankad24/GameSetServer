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
                    self.data[uid] = User(uid,t[1],t[2],t[3])

    def get_by_nick(self, nick):
        users = list(filter(lambda u: u.nickname==nick, self.data.values()))
        if len(users)==1:
            return users[0]
        else:
            return None

    def get_by_id(self, uid):
        if uid in self.data:
            return self.data[uid]
        else:
            return None

    def create_user(self, nickname, password):
        new_id = uuid4().int % 1000000
        while new_id in self.data:
            new_id = uuid4().int % 1000000
        new_user = User(new_id,nickname,password,"")
        self.data[new_id] = new_user
        return new_user

    def save_new_user(self, user):
        with open("users.csv", "a") as f:
            f.write(f"{user.id},{user.nickname},{user.password},{user.token}\n")
