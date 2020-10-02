import pygame
import config
from model import model
from view.view import View
from controller.controller import Controller
from socket import socket, AF_INET, SOCK_STREAM
from config import HOST, PORT, ENCODING
from utils import convert_keys_to_string
from threading import Thread
import struct

view = View()
controller = Controller()

clientsock = socket(AF_INET, SOCK_STREAM)
clientsock.connect((HOST, PORT))

player_id = int.from_bytes(clientsock.recv(1), byteorder="big")
print(f'your id is {player_id}')

map_name = clientsock.recv(config.MAP_NAME_LENGTH).decode(config.ENCODING)
model.game_map.load_selected_map(map_name)

running = True
clock = pygame.time.Clock()


def receiver_thread():
    while running:
        tanks = []
        if int.from_bytes(clientsock.recv(1), byteorder="big") == 0:
            data = clientsock.recv(20 * 8)
            for i in range(0, 20 * 8, 20):
                tank_id = struct.unpack('i', data[i:i + 4])
                x = struct.unpack('f', data[i + 4:i + 8])
                y = struct.unpack('f', data[i + 8:i + 12])
                r = struct.unpack('f', data[i + 12:i + 16])
                keys = data[i + 16:i + 20].decode(config.ENCODING)
                tanks.append((tank_id, x, y, r, keys))

        model.update_tanks(tanks)


receiver = Thread(target=receiver_thread, args=())
receiver.start()

while running:
    events_list = pygame.event.get()
    delta_time = clock.tick(60)

    # Tymaczasowo
    for event in events_list:
        if event.type == pygame.QUIT:
            running = False

    clientsock.send(convert_keys_to_string(pygame.key.get_pressed(), player_id).encode(ENCODING))

    model.update(delta_time)
    view.update()

clientsock.close()
