import pygame
from model import model


class Controller:
    def update(self, delta_time: int):
        pass

    def get_pressed_keys(self, delta_time: int):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            model.move_forward(delta_time)
        elif keys[pygame.K_s]:
            model.move_backward(delta_time)
        elif keys[pygame.K_a]:
            model.move_left(delta_time)
        elif keys[pygame.K_d]:
            model.move_right(delta_time)
