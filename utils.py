import math
from typing import Tuple


def rotate_point(point: Tuple[float, float], angle: float, origin: Tuple[float, float] = (0, 0)):
    radians = angle * math.pi / 180
    s = math.sin(radians)
    c = math.cos(radians)

    px = point[0] - origin[0]
    py = point[1] - origin[1]

    return (
        px * c - py * s + origin[0],
        px * s + py * c + origin[1]
    )
