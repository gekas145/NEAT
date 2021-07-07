import pygame


class Pacman:

    def __init__(self):
        self.radius = 10
        self.x = 100
        self.y = 100
        self.speed = 0.2
        self.vector = 1

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

    def get_xy(self):
        return (self.x, self.y)

    def get_radius(self):
        return self.radius
