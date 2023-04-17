from uuid import uuid4

from flask import session

from data.UserDataSource import UserDataSource


class UserRepository:
    def __init__(self, source: UserDataSource):
        self.users: UserDataSource = source

    @staticmethod
    def is_valid_token(token):
        if ("token" not in session) or (session["token"] != token):
            raise Exception("Invalid token")

    @staticmethod
    def should_be_logged_in():
        if "nick" not in session:
            raise Exception("You need to log in")

    @staticmethod
    def should_be_logged_out():
        if "nick" in session:
            raise Exception("You are logged in")

    def get_token(self):
        self.should_be_logged_in()
        token = uuid4().hex
        session["token"] = token
        return token

    def get_nick(self):
        self.should_be_logged_in()
        return session["nick"]

    def register(self, nick, password):
        self.should_be_logged_out()
        user_password = self.users.get_by_nick(nick)
        if not nick or not password:
            raise Exception("Incorrect request")
        if user_password is not None:
            raise Exception("User already exist")
        else:
            self.users.add(nick,password)
            session["nick"] = nick
        return self.get_token()

    def login(self, nick, password):
        self.should_be_logged_out()
        user_password = self.users.get_by_nick(nick)
        if not nick or not password:
            raise Exception("Incorrect request")
        if user_password is None:
            raise Exception(f"The nickname '{nick}' is not registered")
        elif user_password != password:
            raise Exception("Wrong password")
        else:
            session["nick"] = nick
        return self.get_token()

    def logout(self):
        self.should_be_logged_in()
        session.clear()
