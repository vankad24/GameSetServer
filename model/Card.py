from typing import NamedTuple

class Card:
    def __init__(self,card_id:int, color:int, shape:int, fill:int, count:int):
        self.count = count
        self.fill = fill
        self.shape = shape
        self.color = color
        self.card_id = card_id

    def to_dict(self):
        return {"id":self.card_id,"color":self.color,"shape":self.shape,"fill":self.fill,"count":self.count}