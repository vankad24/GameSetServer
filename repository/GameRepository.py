from model.Game import Game
from model.GameStatus import Status
from repository.ApiException import ApiException

class GameRepository:
    def __init__(self):
        self.last_game_id = 0
        self.games_by_game_id = {}
        self.games_by_user_id = {}

    def should_not_be_in_game(self, uid):
        if uid in self.games_by_user_id:
            raise ApiException("You are in a game already")

    @staticmethod
    def should_not_be_finished(game):
        if game.status == Status.ended:
            raise ApiException("Game finished")

    def get_game_by_id(self, game_id):
        if game_id not in self.games_by_game_id:
            raise ApiException("Wrong game id")
        return self.games_by_game_id[game_id]

    def get_game_by_uid(self, uid):
        if uid in self.games_by_user_id:
            return self.games_by_user_id[uid]
        raise ApiException("You are not in a game")

    def create_game(self, uid):
        self.should_not_be_in_game(uid)
        self.last_game_id+=1
        game = Game(self.last_game_id)
        game.add_player(uid)
        self.games_by_game_id[game.id] = game
        self.games_by_user_id[uid] = game
        return game

    def join_game(self, uid, game_id):
        self.should_not_be_in_game(uid)
        game: Game = self.get_game_by_id(game_id)
        self.should_not_be_finished(game)
        game.add_player(uid)
        self.games_by_user_id[uid] = game
        return game

    def leave_game(self, uid):
        game: Game = self.get_game_by_uid(uid)
        game.remove_player(uid)
        del self.games_by_user_id[uid]
        if game.is_empty():
            del self.games_by_game_id[game.id]

    def get_games(self):
        return self.games_by_game_id.values()

    def pick_cards(self, uid, cards_ids):
        game: Game = self.get_game_by_uid(uid)
        self.should_not_be_finished(game)
        cards = list(filter(lambda card: card.card_id in cards_ids, game.field))
        if len(cards_ids) != 3 or len(set(cards_ids)) != 3 or len(cards) != 3:
            raise ApiException("Wrong card's ids")
        is_set = game.is_set(*cards)
        if is_set:
            game.add_score_by_id(uid,10)
            game.remove_from_field(cards)
            if len(game.deck)>=3 and len(game.field)<12:
                game.add_to_field(3)
            game.check_game_over()
        else:
            if game.get_score_by_id(uid)>0:
                game.add_score_by_id(uid,-1)
        return is_set, game

    def add_three_cards(self, uid):
        game: Game = self.get_game_by_uid(uid)
        self.should_not_be_finished(game)
        if len(game.field) == 21:
            raise ApiException("Maximum 21 cards on the field")
        if len(game.deck) >= 3:
            game.add_to_field(3)
        else:
            raise ApiException("No more cards")

    def find_set(self, uid):
        game: Game = self.get_game_by_uid(uid)
        self.should_not_be_finished(game)
        cards = game.find_set(game.field)
        if cards is None:
            return [], game
        find_set_cost = 0
        score = game.get_score_by_id(uid)
        if score < find_set_cost:
            raise ApiException("Your score should be more than "+str(find_set_cost))
        game.add_score_by_id(uid, -find_set_cost)
        ids = list(map(lambda c: c.card_id, cards))
        return ids, game
