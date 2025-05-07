import time as t
from _thread import *

from player import Player
from chat import Chat


class Round:
    def __init__(self, word: str, player_drawing: Player, game):
        self.word = word
        self.player_drawing = player_drawing
        self.game = game
        self.player_scores = {player: 0 for player in self.game.players}
        self.players_guessed = []
        self.time = 75
        self.chat = Chat(self)
        self.start = t.time()
        start_new_thread(self.time_thread, ())

    def skip(self, player) -> bool:
        if self.player_drawing == player:
            self.chat.update_chat('',
                                  f'Игрок {player.get_name()} пропустил свой ход', False, True)
            return True
        return False

    def get_word(self):
        return self.word

    def get_scores(self):
        return self.player_scores

    def get_score(self, player: Player):
        if player in self.player_scores:
            return self.player_scores[player]
        else:
            raise Exception('Player not in score list')

    def time_thread(self):
        while self.time > 0:
            t.sleep(1)
            self.time -= 1
        self.end_round()

    def message_processing(self, player: Player, msg: str) -> bool:
        correct = self.word.lower() == msg.lower()
        if correct:
            self.players_guessed.append(player)
            player_name = player.get_name()
            self.chat.update_chat(player_name, f'{player_name} отгадал слово', True, True)
            self.player_scores[player] += 1
            return True
        self.chat.update_chat(player.get_name(), msg, False, False)
        return False

    def player_left(self, player: Player) -> None:
        if player in self.player_scores:
            del self.player_scores[player]

        if player in self.players_guessed:
            self.players_guessed.remove(player)

        if player == self.player_drawing:
            self.chat.update_chat('', f'Раунд {self.game.round_count} был пропущен, так как рисовальщик ушёл', False,
                                  True)
            self.end_round()

    def end_round(self):
        for player in self.game.players:
            if player in self.player_scores:
                player.update_score(self.player_scores[player])
        self.game.round_ended()
