import math
from typing import Tuple, List


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


def is_point_inside(vertices: List[Tuple[float, float]], point: Tuple[float, float]) -> bool:
    result = False

    i = 0
    j = len(vertices) - 1

    while i < len(vertices):
        if ((vertices[i][1] > point[1]) != (vertices[j][1] > point[1])) and \
                (point[0] < (vertices[j][0] - vertices[i][0]) * (point[1] - vertices[i][1]) / (vertices[j][1] - vertices[i][1]) + vertices[i][0]):
            result = not result

        j, i = i, i + 1

    return result


def are_colliding(shape1: List[Tuple[float, float]], shape2: List[Tuple[float, float]]) -> bool:
    for point in shape1:
        if is_point_inside(shape2, point):
            return True

    for point in shape2:
        if is_point_inside(shape1, point):
            return True

    return False
