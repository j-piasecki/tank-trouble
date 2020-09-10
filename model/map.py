from typing import List
import glob
import pygame
import random
import config


class Map:
    def __init__(self, width: int = 0, height: int = 0, blocks: List[List[bool]] = None):
        if blocks is None:
            self.width = width
            self.height = height

            self.blocks = []

            for x in range(width):
                self.blocks.append([])
                for y in range(height):
                    self.blocks[x].append(True)
        else:
            self.width = len(blocks)
            self.height = len(blocks[0])

            self.blocks = blocks

        self.load_map()

    def is_passable(self, x: int, y: int) -> bool:
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False

        return self.blocks[x][y]

    def load_map(self):
        maps_names = glob.glob('maps/*.png')
        map_image = pygame.transform.scale(pygame.image.load(random.choice(maps_names)), (self.width, self.height))
        map_pixels = pygame.PixelArray(map_image)

        for x in range(self.width):
            for y in range(self.height):
                self.blocks[x][y] = (map_pixels[x, y] == map_image.map_rgb(config.BLACK))

