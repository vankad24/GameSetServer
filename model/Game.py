from model.Card import Card
from random import shuffle

class Game:
    def __init__(self):
        self.cards = []
        self.field = []
        self.players = []
        self.scores = {}
        self.create_cards()
        self.add_to_field(12)

    def create_cards(self):
        card_id = 0
        for color in range(1,4):
            for shape in range(1,4):
                for fill in range(1,4):
                    for count in range(1,4):
                        self.cards.append(Card(card_id,color,shape,fill,count))
                        card_id+=1
        shuffle(self.cards)

    def add_user(self,uid):
        self.players.append(uid)
        self.scores[uid] = 0

    def remove_user(self,uid):
        self.players.remove(uid)

    def add_to_field(self, num):
        for i in range(num):
            self.field.append(self.cards.pop())

    def get_score_by_id(self, uid):
        return self.scores[uid]

    def add_score_by_id(self, uid, points):
        self.scores[uid]+=points

    @staticmethod
    def is_set(c1, c2, c3):
        d1 = c1.to_dict()
        d2 = c2.to_dict()
        d3 = c3.to_dict()
        for prop in ["count", "color", "shape", "fill"]:
            if d1[prop] == d2[prop]:
                if d2[prop] != d3[prop]:
                    return False
            elif d2[prop] == d3[prop] or d1[prop] == d3[prop]:
                return False
        return True

    def remove_cards(self, cards):
        for card in cards:
            self.field.remove(card)

    def is_not_over(self):
        return True
