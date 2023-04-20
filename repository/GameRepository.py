from flask import session

from data.UserDataSource import UserDataSource
from model.Game import Game
from repository.ApiException import ApiException
from repository.UserRepository import UserRepository

class GameRepository:
    def __init__(self):
        self.last_game_id = 0
        self.games = {}

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
        self.check_game(game)
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

    @staticmethod
    def check_game(game):
        if game.finished:
            raise ApiException("Game finished")

    def get_current_game(self, token):
        self.check_token(token)
        game_id = self.get_current_game_id()
        game = self.get_game_by_id(game_id)
        self.check_game(game)
        return game

    def pick_cards(self, token, cards_ids):
        game: Game = self.get_current_game(token)
        cards = list(filter(lambda card: card.card_id in cards_ids, game.field))
        if len(cards_ids) != 3 or len(set(cards_ids)) != 3 or len(cards) != 3:
            raise ApiException("Wrong card's ids")
        is_set = game.is_set(*cards)
        uid = UserRepository.get_user_id()
        if is_set:
            game.add_score_by_id(uid,10)
            game.remove_from_field(cards)
            if len(game.cards)>=3 and len(game.field)<12:
                game.add_to_field(3)
            game.check_game_over()
        else:
            if game.get_score_by_id(uid)>0:
                game.add_score_by_id(uid,-1)
        score = game.get_score_by_id(uid)
        return is_set, score

    def get_three_cards(self, token):
        game: Game = self.get_current_game(token)
        if len(game.field) == 21:
            raise ApiException("Maximum 21 cards on the field")
        if len(game.cards) >= 3:
            game.add_to_field(3)
        else:
            raise ApiException("No more cards")

    def find_set(self, token):
        game: Game = self.get_current_game(token)
        uid = UserRepository.get_user_id()
        cards = game.find_set(game.field)
        score = game.get_score_by_id(uid)
        if cards is None:
            return None, score
        find_set_cost = 15
        if score < find_set_cost:
            raise ApiException("Your score should be more than "+str(find_set_cost))
        game.add_score_by_id(uid, -find_set_cost)
        ids = list(map(lambda c: c.card_id, cards))
        return ids, game.get_score_by_id(uid)
