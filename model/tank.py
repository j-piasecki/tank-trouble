import config
import utils
from .map import Map


class Tank:
    def __init__(self, x: float = config.PLAYER_SIZE[0] * 0.5, y: float = config.PLAYER_SIZE[1] * 0.5):
        self.width = config.PLAYER_SIZE[0]
        self.height = config.PLAYER_SIZE[1]

        self.x = x
        self.y = y

        self.angle = 0

    def move_forward(self, game_map: Map, distance: float):
        vector = utils.rotate_point((0, -distance), self.angle)
        self.x += vector[0]
        self.y += vector[1]

        self.resolve_collisions(game_map)

    def move_backward(self, game_map: Map, distance: float):
        vector = utils.rotate_point((0, distance), self.angle)
        self.x += vector[0]
        self.y += vector[1]

        self.resolve_collisions(game_map)

    def rotate_left(self, game_map: Map, angle: float):
        self.angle = (self.angle - angle) % 360

    def rotate_right(self, game_map: Map, angle: float):
        self.angle = (self.angle + angle) % 360

    def resolve_collisions(self, game_map: Map):
        if self.y < config.PLAYER_SIZE[1] * 0.5:
            self.y = config.PLAYER_SIZE[1] * 0.5

        if self.y + self.height - config.PLAYER_SIZE[1] * 0.5 > game_map.height:
            self.y = game_map.height - self.height + config.PLAYER_SIZE[1] * 0.5

        if self.x < config.PLAYER_SIZE[0] * 0.5:
            self.x = config.PLAYER_SIZE[0] * 0.5

        if self.x + self.width - config.PLAYER_SIZE[0] * 0.5 > game_map.width:
            self.x = game_map.width - self.width + config.PLAYER_SIZE[0] * 0.5
