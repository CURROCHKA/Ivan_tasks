import socket
import threading
import json
import zlib
import traceback

from player import Player
from game import Game
from config import (
    PLAYERS,
)


class Server:
    def __init__(self):
        self.server = "localhost"
        self.port = 5555
        self.connection_queue = []
        self.game_id = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.server, self.port))
        self.socket.listen()

    def player_thread(self, connection: socket.socket, player: Player) -> None:
        while True:
            try:
                data = connection.recv(2048)
                if not data:
                    break

                data = json.loads(data.decode())
                keys = list(map(int, data.keys()))
                response = {key: [] for key in keys}

                for key in keys:
                    if not player.game:
                        continue
                    match key:
                        case -1:  # get a list of players
                            response[-1] = [p.get_name() for p in player.game.players]

                        case 0:  # guess or text
                            response[0] = [player.game.player_guess(player, data["0"][0])]

                        case 1:  # skip
                            response[1] = player.game.skip(player)

                        case 2:  # get chat new content
                            response[2] = player.game.round.chat.get_new_content()

                        case 3:  # get board
                            board = player.game.board.get_board()
                            response[3] = board

                        case 4:  # get score
                            response[4] = player.game.get_player_scores()

                        case 5:  # get round
                            response[5] = player.game.round_count

                        case 6:  # get word
                            response[6] = player.game.round.get_word()

                        case 7:  # update board
                            if player.game.round.player_drawing == player:
                                x, y, color = data["7"]
                                player.game.update_board(x, y, color)

                        case 8:  # get round time
                            response[8] = player.game.round.time

                        case 9:  # clear board
                            player.game.board.clear()

                        case 10:  # get is_drawing_player
                            response[10] = player.game.round.player_drawing == player

                        case 11:  # set filling in board
                            player.game.board.filling = data["11"]

                response = json.dumps(response)
                compressed_data = zlib.compress(response.encode())
                connection.sendall(len(compressed_data).to_bytes(4, "big"))
                connection.sendall(compressed_data)

            except Exception as e:
                print(f"[EXCEPTION] {player.get_name()}: {e}")
                traceback.print_exc()
                break

        self.disconnect(connection, player)

    def disconnect(self, connection: socket.socket, player: Player) -> None:
        if player.game:
            player.game.player_disconnected(player)

        if player in self.connection_queue:
            self.connection_queue.remove(player)

        print(f"[DISCONNECT] {player.get_name()} disconnected")
        connection.close()

    def handle_queue(self, player: Player) -> None:
        self.connection_queue.append(player)

        if len(self.connection_queue) >= PLAYERS:
            game = Game(self.game_id, self.connection_queue[:PLAYERS])

            for player in game.players:
                player.set_game(game)

            print(f"[GAME] Game {self.game_id} started")
            self.game_id += 1
            self.connection_queue = self.connection_queue[PLAYERS:]

    def authentication(self, connection: socket.socket, address: tuple[str, int]) -> None:
        try:
            data = connection.recv(1024)
            name = str(data.decode())
            if not name:
                raise ValueError("No name received")
            elif name in [player.get_name() for player in self.connection_queue]:
                connection.sendall("-1".encode())
                raise ValueError("This nickname already exist")

            connection.sendall("1".encode())
            player = Player(address, name)
            self.handle_queue(player)
            threading.Thread(target=self.player_thread, args=(connection, player)).start()
        except Exception as e:
            print(f"[EXCEPTION] Error authenticating player {address}: {e}")
            connection.close()

    def connection_thread(self) -> None:
        try:
            print("Server started, waiting for connections...")

            while True:
                connection, address = self.socket.accept()
                print(f"[CONNECT] {address}")
                self.authentication(connection, address)

        except socket.error as e:
            print(f"[ERROR] {e}")
            self.socket.close()


if __name__ == "__main__":
    server = Server()
    threading.Thread(target=server.connection_thread).start()
