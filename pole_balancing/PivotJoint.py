import pymunk


class PivotJoint:
    # code for this class was partially taken from https://pymunk-tutorial.readthedocs.io/en/latest/joint/joint.html
    def __init__(self, space, b, b2, a=(0, 0), a2=(0, 0), collide=False):
        joint = pymunk.constraints.PinJoint(b, b2, a, a2)
        joint.collide_bodies = collide
        joint.distance = 0
        joint.error_bias = pow(0.001, 5)
        space.add(joint)
