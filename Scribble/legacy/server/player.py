class Player:
    def __init__(self, ip, name: str):
        self.game = None
        self.ip = ip
        self.name = name
        self.score = 0

    def set_game(self, game) -> None:
        self.game = game

    def update_score(self, score: int) -> None:
        self.score += score

    def guess(self, word: str) -> bool:
        return self.game.player_guess(self, word)

    def disconnect(self) -> None:
        self.game.player_disconnect(self)

    def get_ip(self):
        return self.ip

    def get_name(self):
        return self.name

    def get_score(self):
        return self.score
