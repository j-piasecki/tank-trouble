import config
import utils
import math
from .map import Map
from typing import Tuple


class Tank:
    def __init__(self, x: float = config.PLAYER_SIZE[0] * 0.5 + 1, y: float = config.PLAYER_SIZE[1] * 0.5 + 1):
        self.width = config.PLAYER_SIZE[0]
        self.height = config.PLAYER_SIZE[1]

        self.x = x
        self.y = y

        self._points = [
            (-self.width / 2, -self.height / 2),
            (self.width / 2, -self.height / 2),
            (self.width / 2, self.height / 2),
            (-self.width / 2, self.height / 2)
        ]

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

        self.resolve_collisions(game_map)

    def rotate_right(self, game_map: Map, angle: float):
        self.angle = (self.angle + angle) % 360

        self.resolve_collisions(game_map)

    def resolve_collisions(self, game_map: Map):
        if self.y < config.PLAYER_SIZE[1] * 0.5:
            self.y = config.PLAYER_SIZE[1] * 0.5

        if self.y + self.height - config.PLAYER_SIZE[1] * 0.5 > game_map.height:
            self.y = game_map.height - self.height + config.PLAYER_SIZE[1] * 0.5

        if self.x < config.PLAYER_SIZE[0] * 0.5:
            self.x = config.PLAYER_SIZE[0] * 0.5

        if self.x + self.width - config.PLAYER_SIZE[0] * 0.5 > game_map.width:
            self.x = game_map.width - self.width + config.PLAYER_SIZE[0] * 0.5

        startx = int(self.x - config.PLAYER_SIZE[0] / 1.5)
        starty = int(self.y - config.PLAYER_SIZE[1] / 1.5)

        endx = int(self.x + config.PLAYER_SIZE[0] / 1.5)
        endy = int(self.y + config.PLAYER_SIZE[1] / 1.5)

        shape = self.get_shape()

        for x in range(startx, endx + 1):
            for y in range(starty, endy + 1):
                if self.is_colliding(game_map, x, y, shape):
                    self.resolve_collision(game_map, x, y)

                    shape = self.get_shape()

    def is_colliding(self, game_map: Map, x: int, y: int, shape=None) -> bool:
        if shape is None:
            shape = self.get_shape()

        if game_map.is_blocked(x, y):
            return utils.are_colliding(game_map.get_block_shape(x, y), shape)

        return False

    def resolve_collision(self, game_map: Map, x: int, y: int):
        points = game_map.get_block_shape(x, y)

        for point in points:
            if utils.is_point_inside(self.get_shape(), point):
                to_origin_vector = (self.x - point[0], self.y - point[1])
                length = math.sqrt(to_origin_vector[0] * to_origin_vector[0] + to_origin_vector[1] * to_origin_vector[1])
                normalized = (to_origin_vector[0] / length, to_origin_vector[1] / length)

                while utils.is_point_inside(self.get_shape(), point):
                    self.x += normalized[0] * 0.1
                    self.y += normalized[1] * 0.1

        for point in self.get_shape():
            if utils.is_point_inside(points, point):
                to_origin_vector = (self.x - point[0], self.y - point[1])
                length = math.sqrt(to_origin_vector[0] * to_origin_vector[0] + to_origin_vector[1] * to_origin_vector[1])
                normalized = (to_origin_vector[0] / length, to_origin_vector[1] / length)

                new_point = point
                while utils.is_point_inside(points, new_point):
                    new_point = (new_point[0] + normalized[0] * 0.02, new_point[1] + normalized[1] * 0.02)

                self.x += new_point[0] - point[0]
                self.y += new_point[1] - point[1]

    def get_point(self, point: int) -> Tuple[float, float]:
        rotated = utils.rotate_point(self._points[point], self.angle)
        return rotated[0] + self.x, rotated[1] + self.y

    def get_shape(self):
        return [self.get_point(0), self.get_point(1), self.get_point(2), self.get_point(3)]
