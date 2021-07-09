import pygame
from pygame import Rect as rc


class Map:

    def __init__(self, width, height):
        left_ls = [0, 23, 103, 203, 23, 103, 123, 143, 203, 3, 3, 103, 23, 63, 3, 103, 23, 103, 143, 203, 143, 203]
        top_ls = [0, 23, 23, 3, 83, 83, 123, 83, 103, 123, 203, 203, 283, 303, 323, 283, 383, 323, 323, 363, 243, 263]
        width_ls = [width, 60, 80, 10, 60, 20, 60, 70, 10, 80, 80, 20, 60, 20, 40, 80, 160, 20, 70, 10, 70, 10]
        height_ls = [height, 40, 40, 60, 20, 100, 20, 20, 40, 60, 60, 60, 20, 60, 40, 20, 20, 60, 40, 40, 20, 40]

        map_start = [pygame.Rect(0, 0, 0, 0)] * len(left_ls)

        for i in range(len(map_start)):
            map_start[i] = rc(left_ls[i], top_ls[i], width_ls[i], height_ls[i])

        map = map_start.copy()
        for i in range(1, len(map)):
            map.append(rc(2*width//2 - left_ls[i] - width_ls[i], top_ls[i], width_ls[i], height_ls[i]))

        map.append(rc(143, 163, 134, 60))

        self.map = map

        self.corners = [[13, 13], [93, 13], [193, 13], [13, 73], [93, 73], [193, 73],
                        [13, 113], [93, 113], [133, 113], [133, 73], [193, 113], [93, 193],
                        [133, 193], [133, 153], [193, 153], [133, 233], [133, 273], [93, 273],
                        [13, 273], [13, 313], [53, 313], [53, 373], [13, 373], [13, 413], [93, 373],
                        [93, 313], [133, 313], [193, 313], [193, 273], [133, 373], [193, 373], [193, 413]]

        for i in range(len(self.corners)):
            self.corners.append([2*width//2 - self.corners[i][0], self.corners[i][1]])

    def get_attributes(self):
        return self.map, self.corners

