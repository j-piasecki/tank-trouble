import config
import time
import random
from os import listdir
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread, Lock
from model import map, tank
from utils import convert_key_string_to_dict


class Client:
    def __init__(self, socket: socket, address, id: int):
        self.socket = socket
        self.address = address
        self.id = id
        self.player = tank.Tank()

        self.socket.setblocking(True)

        self.thread: Thread = Thread(target=self.loop, args=())
        self.running = True

    def start(self, map_name: str):
        # format id: 1byte(int) + file_name: string(file name - config.MAP_NAME_LENGTH(17) bytes)
        self.socket.send(bytes([self.id]) + bytes(map_name, config.ENCODING))
        self.thread.start()

    def loop(self):
        while self.running:
            try:
                # keys data
                # string s: s[0] = id, s[1] = is_w_pressed, s[2] = is_a_pressed,
                # s[3] = is_s_pressed, s[4] = is_d_pressed, s[5] = is_space_pressed
                data = self.socket.recv(6).decode(config.ENCODING)
                (key_pressed, player_id) = convert_key_string_to_dict(data)
                print(player_id)
                print(key_pressed)

                if len(data) == 0:
                    self.stop()
            except ConnectionResetError:
                self.stop()

    def stop(self):
        self.running = False
        self.socket.close()
        print(f"client with id {self.id} disconnected")


class Server:
    def __init__(self):
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind((config.HOST, config.PORT))
        self.server_socket.listen(8)

        self.lock = Lock()
        self.running = False
        self.clients = []

        self.main_thread = Thread(target=self.loop, args=())
        self.accepting_thread = Thread(target=self.accept_clients, args=())

        self.map_name = random.choice(listdir("maps/"))
        self.map = map.Map()

        print(f"loaded map: {self.map_name}")

    def start(self):
        self.running = True

        self.main_thread.start()
        self.accepting_thread.start()

        while self.running:
            cmd = input()

            if cmd == "stop":
                self.running = False
                self.server_socket.close()

                for client in self.clients:
                    client.socket.close()

    def accept_clients(self):
        while self.running:
            (client_socket, address) = self.server_socket.accept()

            client = None

            with self.lock:
                id = len(self.clients)
                # find first free slot in the list
                for i in range(len(self.clients)):
                    if self.clients[i] is None:
                        id = i
                        break

                client = Client(client_socket, address, id)

                print(f"client with id: {id} connected from {address}")

                # if there is no empty slot, append the client to the list
                if id == len(self.clients):
                    self.clients.append(client)
                else:
                    self.clients[id] = client

            client.start(self.map_name)

    def loop(self):
        while self.running:
            with self.lock:
                # remove dead inactive clients from list
                for i in range(len(self.clients)):
                    if self.clients[i] is not None and not self.clients[i].running:
                        self.clients[i] = None

                print("update server")

            time.sleep(5)


if __name__ == "__main__":
    server = Server()

    server.start()
