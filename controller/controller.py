import pygame
from model import model
from socket import socket
from config import ENCODING


class Controller:
    def update(self, delta_time: int):
        pass

    def get_pressed_keys(self, delta_time: int, player_id: int, sock: socket):
        keys = pygame.key.get_pressed()
        key_pressed = ''
        if keys[pygame.K_w]:
            key_pressed = 'W'
        elif keys[pygame.K_s]:
            key_pressed = 'S'

        if keys[pygame.K_a]:
            key_pressed = 'A'
        elif keys[pygame.K_d]:
            key_pressed = 'D'

        if key_pressed:
            key_pressed = key_pressed + '-' + str(player_id)

            sock.send(bytes(key_pressed, encoding=ENCODING))
