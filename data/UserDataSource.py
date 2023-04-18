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
                    self.data[uid] = User(uid,t[1],t[2],"")

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

    def create_new_user(self, nickname, password):
        new_id = uuid4().int
        while new_id in self.data:
            new_id = uuid4().int
        new_user = User(new_id,nickname,password,"")
        self.data[new_id] = new_user
        with open("users.csv", "a") as f:
            f.write(f"{new_id},{nickname},{password}\n")
        return new_user
