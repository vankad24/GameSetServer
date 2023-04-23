from dto.response.GameResponse import GameResponse


class GameFieldResponse(GameResponse):
    def __init__(self, score, game):
        super().__init__(score, game)
        self.left = game.cards_left()
        self.field = game.field

    def to_dict(self):
        d = super().to_dict()
        arr = []
        for card in self.field:
            arr.append(card.to_dict())
        d["cards"] = arr
        d["cardsLeft"] = self.left
        return d