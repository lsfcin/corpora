import numpy as np
import transform

class Camera:
    def __init__(self, width = 640, height = 480):

        # Define position as the origin of the coordinate system
        position = np.array([0, 0, 0])

        # Define orientation as the identity matrix
        orientation = np.eye(3)

        self.transform = transform.Transform(position, orientation)
        
        # Define the resolution of the camera
        self.width = width
        self.height = height

        # Define the intrinsic camera matrix
        self.intrinsic_matrix = np.array([
            [width,    0  ,  width / 2],
            [  0  , height, height / 2],
            [  0  ,    0  ,     1     ]
        ])

        
    def project_point(self, point):
        
        # Create the Rt matrix
        Rt = np.hstack((self.orientation, self.position.reshape(3, 1)))

        # Create the intrinsic matrix
        K = self.intrinsic_matrix