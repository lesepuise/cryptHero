import copy
import random

import numpy as np
import tcod


class BSPGenerator():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.bsp = tcod.bsp.BSP(1, 1, width - 1, height - 1)
        self.map = np.zeros(
            (width, height), dtype=bool, order="F"
        )
        self.generate()
    
    def get_map(self):
        return self.map

    def generate(self):
        self.bsp.children = ()
        self.bsp.split_recursive(8, 10, 10, 1.5, 1.5)
        self.refresh()

    def refresh(self):
        self.map[...] = False
        for node in copy.deepcopy(self.bsp).inverted_level_order():
            self.traverse_node(node)

    def traverse_node(self, node):
        if not node.children:
            node.width -= 1
            node.height -= 1
            new_width = random.randint(min(node.width, 9), node.width)
            new_height = random.randint(min(node.height, 9), node.height)
            node.x += random.randint(0, node.width - new_width)
            node.y += random.randint(0, node.height - new_height)
            node.width, node.height = new_width, new_height
            for x in range(node.x, node.x + node.width):
                for y in range(node.y, node.y + node.height):
                    self.map[x][y] = True
        else:
            left, right = node.children
            node.x = min(left.x, right.x)
            node.y = min(left.y, right.y)
            node.w = max(left.x + left.w, right.x + right.w) - node.x
            node.h = max(left.y + left.h, right.y + right.h) - node.y
            if node.horizontal:
                if left.x + left.w - 1 < right.x or right.x + right.w - 1 < left.x:
                    x1 = random.randint(left.x, left.x + left.w - 1)
                    x2 = random.randint(right.x, right.x + right.w - 1)
                    y = random.randint(left.y + left.h, right.y)
                    self.vline_up(x1, y - 1)
                    self.hline(x1, y, x2)
                    self.vline_down(x2, y + 1)
                else:
                    minx = max(left.x, right.x)
                    maxx = min(left.x + left.w - 1, right.x + right.w - 1)
                    x = random.randint(minx, maxx)
                    self.vline_down(x, right.y)
                    self.vline_up(x, right.y - 1)
            else:
                if left.y + left.h - 1 < right.y or right.y + right.h - 1 < left.y:
                    y1 = random.randint(left.y, left.y + left.h - 1)
                    y2 = random.randint(right.y, right.y + right.h - 1)
                    x = random.randint(left.x + left.w, right.x)
                    self.hline_left(x - 1, y1)
                    self.vline(x, y1, y2)
                    self.hline_right(x + 1, y2)
                else:
                    miny = max(left.y, right.y)
                    maxy = min(left.y + left.h - 1, right.y + right.h - 1)
                    y = random.randint(miny, maxy)
                    self.hline_left(right.x - 1, y)
                    self.hline_right(right.x, y)

    def vline(self, x, y1, y2):
        if y1 > y2:
            y1, y2 = y2, y1
        for y in range(y1, y2 + 1):
            self.map[x][y] = True

    def vline_up(self, x, y):
        while y >= 0 and not self.map[x][y]:
            self.map[x][y] = True
            y -= 1

    def vline_down(self, x, y):
        while y < self.height and not self.map[x][y]:
            self.map[x][y] = True
            y += 1

    def hline(self, x1, y, x2):
        if x1 > x2:
            x1, x2 = x2, x1
        for x in range(x1, x2 + 1):
            self.map[x][y] = True

    def hline_left(self, x, y):
        while x >= 0 and not self.map[x][y]:
            self.map[x][y] = True
            x -= 1

    def hline_right(self, x, y):
        while x < self.width and not self.map[x][y]:
            self.map[x][y] = True
            x += 1