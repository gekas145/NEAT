class Pacman:

    def __init__(self, x, y):
        self.radius = 9.5
        self.x = x
        self.y = y
        self.speed = 1
        self.vector = 2
        self.front_point_x = self.x + self.radius + 1.5
        self.front_point_y = self.y

    def move(self):
        if self.vector == 1:
            self.x -= self.speed
            self.front_point_x -= self.speed
        elif self.vector == 2:
            self.x += self.speed
            self.front_point_x += self.speed
        elif self.vector == 3:
            self.y -= self.speed
            self.front_point_y -= self.speed
        else:
            self.y += self.speed
            self.front_point_y += self.speed

    def set_vector(self, new_vector):
        self.vector = new_vector
        dst = 2
        if self.vector == 1:
            self.front_point_x = self.x - self.radius - dst
            self.front_point_y = self.y
        elif self.vector == 2:
            self.front_point_x = self.x + self.radius + dst
            self.front_point_y = self.y
        elif self.vector == 3:
            self.front_point_x = self.x
            self.front_point_y = self.y - self.radius - dst
        else:
            self.front_point_x = self.x
            self.front_point_y = self.y + self.radius + dst

    def get_xy(self):
        return self.x, self.y

    def get_front_xy(self):
        return self.front_point_x, self.front_point_y

    def get_radius(self):
        return self.radius

    def get_vector(self):
        return self.vector