import src.pose6dof as pose6dof

class Box3D:
    def __init__(self, dimensions, pose6dof):
        self.dimensions = dimensions
        self.pose6dof = pose6dof