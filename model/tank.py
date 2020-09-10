import config
from .map import Map


class Tank:
    def __init__(self, x: float = config.PLAYER_SIZE[0] * 0.5, y: float = config.PLAYER_SIZE[1] * 0.5):
        self.width = config.PLAYER_SIZE[0]
        self.height = config.PLAYER_SIZE[1]

        self.x = x
        self.y = y

    def move_forward(self, game_map: Map, distance: float):
        self.y -= distance

        if self.y < config.PLAYER_SIZE[1] * 0.5:
            self.y = config.PLAYER_SIZE[1] * 0.5

    def move_backward(self, game_map: Map, distance: float):
        self.y += distance

        if self.y + self.height - config.PLAYER_SIZE[1] * 0.5 > game_map.height:
            self.y = game_map.height - self.height + config.PLAYER_SIZE[1] * 0.5

    def move_left(self, game_map: Map, distance: float):
        self.x -= distance

        if self.x < config.PLAYER_SIZE[0] * 0.5:
            self.x = config.PLAYER_SIZE[0] * 0.5

    def move_right(self, game_map: Map, distance: float):
        self.x += distance

        if self.x + self.width - config.PLAYER_SIZE[0] * 0.5 > game_map.width:
            self.x = game_map.width - self.width + config.PLAYER_SIZE[0] * 0.5
