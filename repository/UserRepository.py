
from data.UserDataSource import UserDataSource
from repository.ApiException import ApiException


class UserRepository:
    def __init__(self, source: UserDataSource):
        self.users: UserDataSource = source

    def register(self, nick, password):
        if not nick or not password:
            raise ApiException("Incorrect request")
        user = self.users.get_by_nick(nick)
        if user is not None:
            raise ApiException("User already exist")
        else:
            user = self.users.create_user(nick, password)
            return user

    def login(self, nick, password):
        if not nick or not password:
            raise ApiException("Incorrect request")
        user = self.users.get_by_nick(nick)
        if user is None:
            raise ApiException(f"The nickname '{nick}' is not registered")
        elif user.password != password:
            raise ApiException("Wrong password")
        else:
            return user

    def get_user_by_token(self, token):
        user = self.users.get_by_token(token)
        if user is None:
            raise ApiException("Invalid token")
        return user

