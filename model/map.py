from typing import List


class Map:
    def __init__(self, width: int = 0, height: int = 0, blocks: List[List[bool]] = None):
        if blocks is None:
            self.width = width
            self.height = height

            self.blocks = []

            for x in range(height):
                self.blocks.append([])
                for y in range(width):
                    self.blocks[x].append(True)
        else:
            self.height = len(blocks)
            self.width = len(blocks[0])

            self.blocks = blocks

    def is_passable(self, x: int, y: int) -> bool:
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False

        return self.blocks[x][y]
