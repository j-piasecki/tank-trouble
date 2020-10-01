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
        self.tank_img = pygame.transform.scale(tank, (config.PLAYER_SIZE[0] * config.TILE_SIZE,
                                                      config.PLAYER_SIZE[1] * config.TILE_SIZE))

    def data_to_tanks(self, tanks_data: list) -> list:
        tanks = []
        for data in tanks_data:
            if data[0][0] >= 0:
                tank = model.Tank(data[1][0], data[2][0], data[3][0])
                tanks.append(tank)
        return tanks

    # aktuaizuje zmienne elementy ekranu
    def update(self, tanks_data: list):
        self.screen.fill(config.WHITE)

        for i in range(model.game_map.height):
            for j in range(model.game_map.width):
                if model.game_map.is_blocked(j, i):
                    pygame.draw.rect(self.screen, config.BLACK,
                                     (j * config.TILE_SIZE,
                                      i * config.TILE_SIZE,
                                      config.TILE_SIZE,
                                      config.TILE_SIZE))

        tanks = self.data_to_tanks(tanks_data)
        for tank in tanks:
            tmp_tank = pygame.transform.rotate(self.tank_img, -tank.angle)
            rect = tmp_tank.get_rect()
            self.screen.blit(tmp_tank, (tank.x * config.TILE_SIZE - rect.width / 2,
                                        tank.y * config.TILE_SIZE - rect.height / 2))

        pygame.display.update()
