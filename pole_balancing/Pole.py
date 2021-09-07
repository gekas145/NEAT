import pymunk


class Pole:
    # code for this class was taken from https://pymunk-tutorial.readthedocs.io/en/latest/joint/joint.html
    # (the class is named as `Segment` there)
    def __init__(self, space, p0, v, radius=10):
        self.body = pymunk.Body()
        self.body.position = p0
        shape = pymunk.Segment(self.body, (0, 0), v, radius)
        shape.density = 0.1
        shape.elasticity = 0.5
        shape.filter = pymunk.ShapeFilter(group=1)
        shape.color = (0, 255, 0, 0)
        space.add(self.body, shape)
