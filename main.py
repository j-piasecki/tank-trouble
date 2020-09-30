import pygame
import config
from model import model
from view.view import View
from controller.controller import Controller
from socket import socket, AF_INET, SOCK_STREAM
from config import HOST, PORT, ENCODING

view = View()
controller = Controller()

times = [pygame.time.get_ticks(), pygame.time.get_ticks()]

clientsock = socket(AF_INET, SOCK_STREAM)
clientsock.connect((HOST, PORT))

player_id = int.from_bytes(clientsock.recv(1), byteorder="big")
print(f'your id is {player_id}')

map_name = clientsock.recv(config.MAP_NAME_LENGTH).decode(config.ENCODING)
model.game_map.load_selected_map(map_name)

running = True
clock = pygame.time.Clock()

while running:
    events_list = pygame.event.get()
    delta_time = clock.tick(60)

    # Tymaczasowo
    for event in events_list:
        if event.type == pygame.QUIT:
            running = False

    controller.get_pressed_keys(delta_time, player_id, clientsock)
    view.update()

clientsock.close()
