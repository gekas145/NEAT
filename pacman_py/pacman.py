import pygame


class Pacman:

    def __init__(self):
        self.radius = 9.9
        self.x = 13
        self.y = 13
        self.speed = 0.2
        self.vector = 2
        self.front_point_x = self.x + self.radius + 3
        self.front_point_y = self.y

    def move(self):
        if self.vector == 1:
            self.x -= self.speed
        elif self.vector == 2:
            self.x += self.speed
        elif self.vector == 3:
            self.y -= self.speed
        else:
            self.y += self.speed

    def set_vector(self, new_vector):
        self.vector = new_vector
        if self.vector == 1:
            self.front_point_x = self.x - self.radius - 3
            self.front_point_y = self.y
        elif self.vector == 2:
            self.front_point_x = self.x + self.radius + 3
            self.front_point_y = self.y
        elif self.vector == 3:
            self.front_point_x = self.x
            self.front_point_y = self.y - self.radius - 3
        else:
            self.front_point_x = self.x
            self.front_point_y = self.y + self.radius + 3

    def get_xy(self):
        return self.x, self.y

    def get_front_xy(self):
        return self.front_point_x, self.front_point_y

    def get_radius(self):
        return self.radius
