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

        tank = pygame.image.load('view/images/tank.png')
        self.tank_img = pygame.transform.scale(tank, (config.PLAYER_SIZE[0] * config.TILE_SIZE, config.PLAYER_SIZE[1] * config.TILE_SIZE))

    # aktuaizuje zmienne elementy ekranu
    def update(self):
        self.screen.fill(config.WHITE)

        self.screen.blit(self.tank_img, ((model.player.x - config.PLAYER_SIZE[0] / 2) * config.TILE_SIZE,
                                         (model.player.y - config.PLAYER_SIZE[1] / 2) * config.TILE_SIZE))

        pygame.display.update()
