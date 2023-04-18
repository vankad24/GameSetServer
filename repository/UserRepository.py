from uuid import uuid4

from flask import session

from data.UserDataSource import UserDataSource
from model.User import User
from repository.ApiException import ApiException


class UserRepository:
    def __init__(self, source: UserDataSource):
        self.users: UserDataSource = source

    @staticmethod
    def should_be_logged_in():
        if "token" not in session:
            raise ApiException("You need to log in")

    @staticmethod
    def should_be_logged_out():
        if "token" in session:
            raise ApiException("You are logged in")

    @staticmethod
    def authorize_user(user: User):
        if not user.token:
            user.token = uuid4().hex
        session["token"] = user.token
        session["nick"] = user.nickname
        session["uid"] = user.id

    @staticmethod
    def get_user_id():
        return session["uid"]

    def register(self, nick, password):
        self.should_be_logged_out()
        if not nick or not password:
            raise ApiException("Incorrect request")
        user = self.users.get_by_nick(nick)
        if user is not None:
            raise ApiException("User already exist")
        else:
            user = self.users.create_new_user(nick, password)
            self.authorize_user(user)
            return user

    def login(self, nick, password):
        self.should_be_logged_out()
        if not nick or not password:
            raise ApiException("Incorrect request")
        user = self.users.get_by_nick(nick)
        if user is None:
            raise ApiException(f"The nickname '{nick}' is not registered")
        elif user.password != password:
            raise ApiException("Wrong password")
        else:
            self.authorize_user(user)
            return user

    def logout(self):
        self.should_be_logged_in()
        session.clear()

    @staticmethod
    def main():
        name = "unknown user"
        if "nick" in session:
            name = session["nick"]
        return f"<h1>Hello, {name}!</h1>"
