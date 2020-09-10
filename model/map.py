import glob
import pygame
import random
import config


class Map:
    def __init__(self, width: int = 0, height: int = 0):
        self.width = width
        self.height = height

        self.load_map()

    def load_map(self):
        maps_names = glob.glob('maps/*.png')
        map_image = pygame.image.load(random.choice(maps_names))
        map_pixels = pygame.PixelArray(map_image)
        for x in range(self.width):
            for y in range(self.height):
                self.blocks[x][y] = (map_pixels[x, y] == map_image.map_rgb(config.BLACK))
