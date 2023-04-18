class Error:
    def __init__(self, msg):
        self.message = msg

    def to_dict(self):
        return {"message":self.message}