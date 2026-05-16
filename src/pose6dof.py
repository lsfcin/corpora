# Pose6DOF: 6-degree-of-freedom pose with position and direction vectors
class Pose6DOF:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction