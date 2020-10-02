import config
from typing import List
from .tank import Tank
from .map import Map

game_map = Map(100, 70)
tanks = []


def update(delta_time: int):
    for tank in tanks:
        if tank.keys[0] == "1":
            tank.move_forward(game_map, delta_time * config.PLAYER_SPEED / config.TILE_SIZE * 0.25)
        if tank.keys[1] == "1":
            tank.rotate_left(game_map, delta_time * config.PLAYER_ROTATION_SPEED * 0.25)
        if tank.keys[2] == "1":
            tank.move_backward(game_map, delta_time * config.PLAYER_SPEED / config.TILE_SIZE * 0.25)
        if tank.keys[3] == "1":
            tank.rotate_right(game_map, delta_time * config.PLAYER_ROTATION_SPEED * 0.25)


def update_tanks(tanks_data: List):
    new_tanks = []
    for data in tanks_data:
        if data[0][0] >= 0:
            tank = Tank(data[0][0], data[1][0], data[2][0], data[3][0], data[4])
            new_tanks.append(tank)

    global tanks
    tanks = new_tanks
