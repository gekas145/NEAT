from pygame import Rect as rc


class Map:

    def __init__(self, width, height):
        left = [0, 23, 103, 203, 23]
        top = [0, 23, 23, 3, 83]
        width = [width, 60, 80, 10, 60]
        height = [height, 40, 40, 60, 20]

        map = [0] * len(left)

        for i in range(len(map)):
            map[i] = rc(left[i], top[i], width[i], height[i])

        self.map = map

    def get_map(self):
        return self.map
