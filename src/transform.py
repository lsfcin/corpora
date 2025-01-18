import cv2
import numpy as np

class Pose6DOF:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        
class Transform:
    def __init__(self, position, orientation):
        
        # Position is a 3x1 numpy matrix
        # Guaranteee that the position to be a column vector of floats
        self.position = np.matrix(position, dtype=np.float32).reshape(3, 1)

        # Orientation is a 3x3 numpy matrix
        # Guaranteee that the orientation to be a 3x3 matrix of floats
        self.orientation = np.matrix(orientation, dtype=np.float32).reshape(3, 3)

    def get_rvec(self):
        rvec = np.zeros((3, 1))
        cv2.Rodrigues(self.orientation, rvec)
        return rvec
    
    def set_rvec(self, rvec):
        self.orientation = cv2.Rodrigues(rvec)[0]

    def get_tvec(self):
        tvec = -(self.orientation * self.position)
        return tvec

    def set_tvec(self, tvec):
        r_transposed = self.orientation.transposed()
        self.position = -r_transposed * tvec

    def get_Rt(self):
        # create a 3x4 matrix [R | t] using the orientation and position
        t = self.get_tvec()
        R = self.orientation
        Rt = np.hstack((R, t))
        return Rt
    
    def move_global(self, translation):
        # Update the position
        self.position += translation

    def move_local(self, translation):
        # Update the position
        self.position += self.orientation @ translation

    def move_forward(self, distance):
        # Update the position
        forward = np.array(self.orientation[:, 2], dtype=np.float32).reshape(3, 1)
        #print("self.position", self.position)
        #print("forward", forward)

        self.position += forward * distance
        #print("self.position", self.position)

    def move_sideward(self, distance):
        # Update the position
        self.position += self.orientation[:, 0] * distance

    def move_upward(self, distance):
        # Update the position
        self.position += self.orientation[:, 1] * distance

    def rotate_global(self, rotation):
        # Update the orientation
        self.orientation = rotation @ self.orientation

    def rotate_axis(self, angle, axis):
        # Create the rotation matrix
        rotation = cv2.Rodrigues(angle * axis)[0]

        # Update the orientation
        self.orientation = rotation @ self.orientation