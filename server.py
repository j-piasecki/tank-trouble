import config
import time
import random
from os import listdir
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread, Lock
from model import map, tank, projectile
from utils import convert_key_string_to_dict
import struct


class Client:
    def __init__(self, socket: socket, address, id: int, map: map.Map):
        self.socket = socket
        self.address = address
        self.id = id
        self.map = map
        self.player = tank.Tank(id, map.spawn_points[id][0], map.spawn_points[id][1])
        self.shoot_time = 0
        self.keys = {
            'up': 0,
            'left': 0,
            'down': 0,
            'right': 0,
            'space': 0
        }

        self.positions = []

        self.socket.setblocking(True)

        self.thread: Thread = Thread(target=self.loop, args=())
        self.running = True

    def start(self, map_name: str):
        # format id: 1byte(int) + file_name: string(file name - config.MAP_NAME_LENGTH(17) bytes)
        self.socket.send(bytes([self.id]) + bytes(map_name, config.ENCODING))
        self.thread.start()

    def send_all_players_info(self):
        try:
            message = bytes([0])
            for i in range(8):
                message = message + struct.pack("i", self.positions[i]["id"]) \
                          + struct.pack("f", self.positions[i]["x"]) \
                          + struct.pack("f", self.positions[i]["y"]) \
                          + struct.pack("f", self.positions[i]["angle"]) \
                          + bytes(f"{self.keys['up']}{self.keys['left']}{self.keys['down']}{self.keys['right']}", encoding=config.ENCODING)
            self.socket.send(message)
        except ConnectionResetError:
            self.stop()
        except ConnectionAbortedError:
            self.stop()

    def send_all_projectiles(self, projectiles: list):
        try:
            message = bytes([1])
            message = message + struct.pack("i", len(projectiles))
            for projectile in projectiles:
                message = message + struct.pack("f", projectile.x) + struct.pack("f", projectile.y)
            self.socket.send(message)
        except ConnectionResetError:
            self.stop()
        except ConnectionAbortedError:
            self.stop()

    def loop(self):
        while self.running:
            try:
                # keys data
                # string s: s[0] = id, s[1] = is_w_pressed, s[2] = is_a_pressed,
                # s[3] = is_s_pressed, s[4] = is_d_pressed, s[5] = is_space_pressed
                data = self.socket.recv(6).decode(config.ENCODING)
                if len(data) == 0:
                    self.stop()
                    break

                if len(data) == 6:
                    (key_pressed, player_id) = convert_key_string_to_dict(data)
                    self.keys = key_pressed

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
        self.projectiles = []

        self.main_thread = Thread(target=self.loop, args=())
        self.accepting_thread = Thread(target=self.accept_clients, args=())

        self.map_name = random.choice(listdir("maps/"))
        self.map = map.Map(100, 70)
        self.map.load_selected_map(self.map_name)

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

                client = Client(client_socket, address, id, self.map)

                print(f"client with id: {id} connected from {address}")

                # if there is no empty slot, append the client to the list
                if id == len(self.clients):
                    self.clients.append(client)
                else:
                    self.clients[id] = client

            client.start(self.map_name)

    def loop(self):
        delta_time = 0.02
        while self.running:
            with self.lock:
                # remove dead inactive clients from list
                for i in range(len(self.clients)):
                    if self.clients[i] is not None and not self.clients[i].running:
                        self.clients[i] = None

                # list of dicts of positions of all players
                positions = []
                err_id = -1
                # non existing clients has ids smaller than zero
                for i in range(8):
                    positions.append({
                        'id': err_id,
                        'x': 0,
                        'y': 0,
                        'angle': 0
                    })
                    err_id = err_id - 1
                for i in range(len(self.clients)):
                    if self.clients[i] is not None:
                        # transaltes key input to player moves
                        if self.clients[i].keys["up"] == 1:
                            self.clients[i].player.move_forward(self.map,
                                                                delta_time * 1000 * config.PLAYER_SPEED / config.TILE_SIZE)
                        if self.clients[i].keys["down"] == 1:
                            self.clients[i].player.move_backward(self.map,
                                                                 delta_time * 1000 * config.PLAYER_SPEED / config.TILE_SIZE)
                        if self.clients[i].keys["right"] == 1:
                            self.clients[i].player.rotate_right(self.map,
                                                                delta_time * 1000 * config.PLAYER_ROTATION_SPEED)
                        if self.clients[i].keys["left"] == 1:
                            self.clients[i].player.rotate_left(self.map,
                                                               delta_time * 1000 * config.PLAYER_ROTATION_SPEED)
                        if self.clients[i].keys["space"] == 1 and time.time() * 1000 - self.clients[i].shoot_time > 1000:
                            self.shoot(self.clients[i])

                        positions[i] = {
                            'id': self.clients[i].id,
                            'x': self.clients[i].player.x,
                            'y': self.clients[i].player.y,
                            'angle': self.clients[i].player.angle
                        }

                for proj in self.projectiles:
                    proj.update(self.map, delta_time * 1000)

                self.projectiles = [x for x in self.projectiles if x.exists]

                for i in range(len(self.clients)):
                    if self.clients[i] is not None:
                        self.clients[i].positions = positions
                        self.clients[i].send_all_players_info()
                        self.clients[i].send_all_projectiles(self.projectiles)

                #print(positions)
                #print("update server")

            time.sleep(delta_time)

    def shoot(self, client):
        client.shoot_time = time.time() * 1000
        proj = projectile.Projectile(client.player.x, client.player.y, client.player.angle)
        self.projectiles.append(proj)


if __name__ == "__main__":
    server = Server()

    server.start()
