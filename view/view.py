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
        self.tank_img = []
        for i in range(8):
            tank = pygame.image.load(f'view/images/tank{i}.png')
            tank = pygame.transform.scale(tank, (config.PLAYER_SIZE[0] * config.TILE_SIZE,
                                                 config.PLAYER_SIZE[1] * config.TILE_SIZE))
            self.tank_img.append(tank)

    # aktuaizuje zmienne elementy ekranu
    def update(self):
        self.screen.fill(config.WHITE)

        for i in range(model.game_map.height):
            for j in range(model.game_map.width):
                if model.game_map.is_blocked(j, i):
                    pygame.draw.rect(self.screen, config.BLACK,
                                     (j * config.TILE_SIZE,
                                      i * config.TILE_SIZE,
                                      config.TILE_SIZE,
                                      config.TILE_SIZE))

        for tank in model.tanks:
            tmp_tank = pygame.transform.rotate(self.tank_img[tank.id], -tank.angle)
            rect = tmp_tank.get_rect()
            self.screen.blit(tmp_tank, (tank.x * config.TILE_SIZE - rect.width / 2,
                                        tank.y * config.TILE_SIZE - rect.height / 2))

        for projectile in model.projectiles:

            pygame.draw.circle(self.screen,
                               config.RED,
                               (int(projectile.x * config.TILE_SIZE), int(projectile.y * config.TILE_SIZE)),
                               int(config.PROJECTILE_SIZE * config.TILE_SIZE))

        pygame.display.update()
