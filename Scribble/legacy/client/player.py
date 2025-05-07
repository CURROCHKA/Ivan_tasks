class Player:
    def __init__(self, name: str):
        self.name = name.strip()
        self.score = 0

    def update_score(self, score: int):
        self.score = score

    def get_score(self):
        return self.score

    def get_name(self):
        return self.name
