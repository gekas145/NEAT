from pygame import Rect as rc

class Map:

    def __init__(self):

        left = [20, 100]
        top = [20, 20]
        width = [60, 80]
        height = [40, 40]

        map = [0] * 2

        for i in range(len(map)):
            map[i] = rc(left[i], top[i], width[i], height[i])

        self.map = map

    def get_map(self):
        return self.map


