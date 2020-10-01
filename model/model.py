import config
from typing import List
from .tank import Tank
from .map import Map

game_map = Map(100, 70)
tanks = []


def update(delta_time: int, tanks_data: List):
    new_tanks = []
    for data in tanks_data:
        if data[0][0] >= 0:
            tank = Tank(data[0][0], data[1][0], data[2][0], data[3][0])
            new_tanks.append(tank)

    global tanks
    tanks = new_tanks
