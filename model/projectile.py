import config
import utils
from .map import Map

class Projectile:
    def __init__(self, x: float, y: float, direction: float):
        self.x = x
        self.y = y
        self.direction = direction

        self.exists = True

    def update(self, game_map: Map, delta_time):
        vector = utils.rotate_point((0, -config.PROJECTILE_SPEED / config.TILE_SIZE * delta_time), self.direction)
        self.x += vector[0]
        self.y += vector[1]

        if self.x < -3 or self.y < -3 or self.x > game_map.width + 3 or self.y > game_map.height + 3:
            self.exists = False
