from flask import session

from data.UserDataSource import UserDataSource
from model.Game import Game
from repository.ApiException import ApiException
from repository.UserRepository import UserRepository

class GameRepository:
    def __init__(self,source: UserDataSource):
        self.last_game_id = 0
        self.games = {}
        self.users: UserDataSource = source

    @staticmethod
    def check_token(token):
        UserRepository.should_be_logged_in()
        if session["token"] != token:
            raise ApiException("Invalid token")

    @staticmethod
    def should_be_in_game():
        if "game_id" not in session:
            raise ApiException("You are not in a game")

    @staticmethod
    def should_not_be_in_game():
        if "game_id" in session:
            raise ApiException("You are in a game already")

    @staticmethod
    def get_current_game_id():
        GameRepository.should_be_in_game()
        return session["game_id"]

    def get_game_by_id(self, game_id):
        if game_id not in self.games:
            raise ApiException("Wrong game id")
        return self.games[game_id]

    def create(self, token):
        self.check_token(token)
        game = Game()
        self.last_game_id+=1
        self.games[self.last_game_id] = game
        return self.last_game_id

    def join_game(self, token, game_id):
        self.check_token(token)
        self.should_not_be_in_game()
        game:Game = self.get_game_by_id(game_id)
        uid = UserRepository.get_user_id()
        game.add_user(uid)
        session["game_id"] = game_id

    def leave_game(self, token):
        self.check_token(token)
        game_id = self.get_current_game_id()
        game = self.get_game_by_id(game_id)
        uid = UserRepository.get_user_id()
        game.remove_user(uid)
        del session["game_id"]
        return game_id

    def get_games_ids(self, token):
        self.check_token(token)
        return self.games.keys()

    def get_current_game(self, token):
        self.check_token(token)
        game_id = self.get_current_game_id()
        return self.get_game_by_id(game_id)

    def pick_cards(self, token, cards_ids):
        game:Game = self.get_current_game(token)
        cards = list(filter(lambda card: card.card_id in cards_ids, game.field))
        if len(cards_ids) != 3 or len(cards) != 3:
            raise ApiException("Wrong card's ids")
        is_set = game.is_set(*cards)
        uid = UserRepository.get_user_id()
        if is_set:
            game.add_score_by_id(uid,10)
            game.remove_cards(cards)
            if game.is_not_over():
                game.add_to_field(3)
        score = game.get_score_by_id(uid)
        return is_set, score

