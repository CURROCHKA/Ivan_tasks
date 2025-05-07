class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.score = 0

    def add_score(self, score: int) -> None:
        self.score += score

    def get_score(self) -> int:
        return self.score

    def get_name(self) -> str:
        return self.name
