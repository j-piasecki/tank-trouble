import pygame
import config
from model import model


class View:

    # inicjalizuje pygame oraz tworzy ekran i ustawia jego paramtery
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (model.game_map.width * config.TILE_SIZE, model.game_map.height * config.TILE_SIZE))

        pygame.display.set_caption("Tank Trouble")

        logo = pygame.image.load('view/images/logo.jpg')
        pygame.display.set_icon(logo)

    # aktuaizuje zmienne elementy ekranu
    def update(self):
        self.screen.fill(config.WHITE)

        pygame.draw.rect(self.screen, config.RED,
                         (model.player.x * config.TILE_SIZE,
                          model.player.y * config.TILE_SIZE,
                          int(model.player.width * config.TILE_SIZE),
                          int(model.player.height * config.TILE_SIZE)))

        pygame.display.update()
