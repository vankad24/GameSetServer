from model.User import User


class UserDataSource:
    def __init__(self):
        self.data = {}
        with open("users.csv") as f:
            f.readline()
            for line in f:
                line = line.strip(" \t\n")
                if line != "":
                    t = line.split(",")
                    self.data[t[0]] = t[1]

    def get_by_nick(self, nick):
        if nick in self.data:
            return self.data[nick]
        else:
            return None

    # def get_by_id(self, uid):
    #     ...
    #
    # def get_by_token(self, token):
    #     ...

    def add(self, nick, password):
        self.data[nick] = password
        with open("users.csv", "a") as f:
            f.write(nick + "," + password + "\n")