import config
from .tank import Tank
from .map import Map

player = Tank()
game_map = Map(100, 70)

def update(delta_time: int):
    pass


def move_forward(delta_time: int):
    player.move_forward(game_map, delta_time * config.PLAYER_SPEED / config.TILE_SIZE)


def move_backward(delta_time: int):
    player.move_backward(game_map, delta_time * config.PLAYER_SPEED / config.TILE_SIZE)


def rotate_left(delta_time: int):
    player.rotate_left(game_map, delta_time * config.PLAYER_ROTATION_SPEED)


def rotate_right(delta_time: int):
    player.rotate_right(game_map, delta_time * config.PLAYER_ROTATION_SPEED)
