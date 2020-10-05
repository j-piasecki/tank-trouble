import config

class Projectile:
    def __init__(self, x: float, y: float, direction: float):
        self.x = x
        self.y = y
        self.direction = direction

    def update(self, delta_time):
        pass
