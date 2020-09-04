import pygame
import config
from model import model


class View:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (model.game_map.width * config.TILE_SIZE, model.game_map.height * config.TILE_SIZE))

        pygame.display.set_caption("Tank Trouble")

        logo = pygame.image.load('images/logo.jpg')
        pygame.display.set_icon(logo)

    def update(self):
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (model.player.x, model.player.y, int(model.player.width * config.TILE_SIZE),
                          int(model.player.height * config.TILE_SIZE)))
        pygame.display.update()
