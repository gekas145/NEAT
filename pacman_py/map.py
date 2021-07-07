from pygame import Rect as rc

class Map:

    def __init__(self, width, height):

        left = [0, 23, 103]
        top = [0, 23, 23]
        width = [width, 60, 80]
        height = [height, 40, 40]

        map = [0] * 3

        for i in range(len(map)):
            map[i] = rc(left[i], top[i], width[i], height[i])

        self.map = map

    def get_map(self):
        return self.map


