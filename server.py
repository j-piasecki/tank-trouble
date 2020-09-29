import config
import time
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread, Lock


class Client:
    def __init__(self, socket: socket, address, id: int):
        self.socket = socket
        self.address = address
        self.id = id

        self.thread: Thread = Thread(target=self.loop, args=())

    def start(self):
        self.socket.send(bytes(str(self.id), config.ENCODING))
        self.thread.start()

    def loop(self):
        while True:
            data = self.socket.recv(3).decode(config.ENCODING)
            print(data)

            if len(data) == 0:
                self.socket.close()
                print(f"client with id {self.id} disconnected")
                break


class Server:
    def __init__(self):
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind((config.HOST, config.PORT))
        self.server_socket.listen(8)

        self.lock = Lock()
        self.running = False
        self.clients = []

        self.thread = Thread(target=self.loop, args=())

    def start(self):
        self.running = True
        self.thread.start()

        while self.running:
            self.accept_client()

    def accept_client(self):
        (client_socket, address) = self.server_socket.accept()

        client = None

        with self.lock:
            id = len(self.clients)
            client = Client(client_socket, address, id)

            print(f"client with id: {id} connected from {address}")

            self.clients.append(client)

        client.start()


    def loop(self):
        while self.running:
            with self.lock:
                print("update server")

            time.sleep(1)


if __name__ == "__main__":
    server = Server()

    server.start()
