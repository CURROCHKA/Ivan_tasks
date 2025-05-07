import socket
import json
import zlib


class Network:
    def __init__(self, name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = 'localhost'
        self.port = 5555
        self.address = (self.server, self.port)
        self.name = name
        self.connection_response = self.connect()

    def connect(self):
        try:
            self.client.connect(self.address)
            self.client.sendall(self.name.encode())
            return json.loads(self.client.recv(1024))
        except Exception as e:
            self.disconnect(f'Connection error: {e}')

    def send(self, data: dict):
        try:
            self.client.send(json.dumps(data).encode())

            data_len = int.from_bytes(self.client.recv(4), 'big')
            compressed_data = self.client.recv(data_len)
            decompressed_data = zlib.decompress(compressed_data).decode()

            return list(json.loads(decompressed_data).values())[0]
        except (socket.error, json.JSONDecodeError, zlib.error) as e:
            self.disconnect(f'Send error: {e}')

    def disconnect(self, msg: str):
        print(f'[EXCEPTION] Disconnected from server: {msg}')
        self.client.close()
