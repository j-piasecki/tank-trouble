import config
from .map import Map


class Tank:
    def __init__(self, x: float = 0, y: float = 0):
        self.width = config.PLAYER_SIZE[0]
        self.height = config.PLAYER_SIZE[1]

        self.x = x
        self.y = y

    def move_forward(self, game_map: Map, distance: float):
        self.y -= distance

        if self.y < 0:
            self.y = 0

    def move_backward(self, game_map: Map, distance: float):
        self.y += distance

        if self.y + self.height > game_map.height:
            self.y = game_map.height - self.height

    def move_left(self, game_map: Map, distance: float):
        self.x -= distance

        if self.x < 0:
            self.x = 0

    def move_right(self, game_map: Map, distance: float):
        self.x += distance

        if self.x + self.width > game_map.width:
            self.x = game_map.width - self.width
