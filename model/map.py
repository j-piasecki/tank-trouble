from typing import List, Tuple
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
            self.spawn_points = []

            for x in range(width):
                self.blocks.append([])
                for y in range(height):
                    self.blocks[x].append(False)
        else:
            self.width = len(blocks)
            self.height = len(blocks[0])

            self.blocks = blocks

    def is_blocked(self, x: int, y: int) -> bool:
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True

        return self.blocks[x][y]

    def get_block_shape(self, x: int, y: int) -> List[Tuple[float, float]]:
        return [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]

    def load_selected_map(self, file_name: str):
        map_image = pygame.image.load(f"maps/{file_name}")

        for x in range(self.width):
            for y in range(self.height):
                self.blocks[x][y] = (map_image.map_rgb(map_image.get_at((x, y))) == map_image.map_rgb(config.BLACK))
                #sprawdzanie czy punkt jest spawn pointem
                if map_image.map_rgb(map_image.get_at((x, y))) == map_image.map_rgb(config.RED):
                    self.spawn_points.append((x, y))
