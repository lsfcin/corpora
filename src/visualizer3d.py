import cv2
import numpy as np

class Cube:
    def __init__(self, top_left_front, bottom_right_back):
        self.top_left_front = top_left_front
        self.bottom_right_back = bottom_right_back
        self.points = [
            self.top_left_front,
            [self.bottom_right_back[0], self.top_left_front[1], self.top_left_front[2]],
            [self.top_left_front[0], self.bottom_right_back[1], self.top_left_front[2]],
            [self.top_left_front[0], self.top_left_front[1], self.bottom_right_back[2]],
            [self.bottom_right_back[0], self.bottom_right_back[1], self.top_left_front[2]],
            [self.bottom_right_back[0], self.top_left_front[1], self.bottom_right_back[2]],
            [self.top_left_front[0], self.bottom_right_back[1], self.bottom_right_back[2]],
            self.bottom_right_back
        ]

        # Define edges of the cube (pairs of indices)
        self.edges = [
            (0, 1), (1, 3), (3, 2), (2, 0),  # Back face
            (4, 5), (5, 7), (7, 6), (6, 4),  # Front face
            (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting edges
        ]

class Visualizer3D:
    def __init__(self):
        self.cube = Cube([0, 0, 0], [1, 1, 1])

        # Camera settings
        self.focal_length = 500
        self.center = (300, 300)
        self.camera_matrix = np.array([
            [self.focal_length, 0, self.center[0]],
            [0, self.focal_length, self.center[1]],
            [0, 0, 1]
        ], dtype=np.float32)

        # Rotation and translation
        self.rotation_vector = np.zeros((3, 1), dtype=np.float32)  # No initial rotation
        self.translation_vector = np.array([[0], [0], [5]], dtype=np.float32)  # Translate away from the camera

        # Mouse interaction
        self.angle_x, self.angle_y = 0.0, 0.0  # Ensure these are floats

        cv2.namedWindow("3D Cube")
        cv2.setMouseCallback("3D Cube", self.mouse_callback)

        # Rotation and translation
        self.rotation_vector = np.zeros((3, 1), dtype=np.float32)  # No initial rotation
        self.translation_vector = np.array([[0], [0], [5]], dtype=np.float32)  # Translate away from the camera

        # Mouse interaction
        self.angle_x, self.angle_y = 0.0, 0.0  # Ensure these are floats

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
            self.angle_x += (y - self.center[1]) * 0.001
            self.angle_y += (x - self.center[0]) * 0.001

    def show(self, cubes, colors):

        # Convert angles to np.float32 for consistency
        rotation_matrix_x = cv2.Rodrigues(np.array([angle_x, 0, 0], dtype=np.float32))[0]
        rotation_matrix_y = cv2.Rodrigues(np.array([0, angle_y, 0], dtype=np.float32))[0]
        rotation_matrix = rotation_matrix_y @ rotation_matrix_x
        rotation_vector, _ = cv2.Rodrigues(rotation_matrix)

        # Create blank image
        img = np.zeros((600, 600, 3), dtype=np.uint8)

        for cube, color in zip(cubes, colors):        
            # Project 3D points to 2D
            projected_points, _ = cv2.projectPoints(cube.points, self.rotation_vector, self.translation_vector, self.camera_matrix, None)
            projected_points = projected_points.reshape(-1, 2)
            
            # Draw edges
            for edge in cube.edges:
                pt1 = tuple(projected_points[edge[0]].astype(int))
                pt2 = tuple(projected_points[edge[1]].astype(int))
                cv2.line(img, pt1, pt2, (0, 255, 0), 2)

        # Show the image
        cv2.imshow("3D Cube", img)



def mouse_callback(event, x, y, flags, param):
    global angle_x, angle_y
    if event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        angle_x += (y - center[1]) * 0.001
        angle_y += (x - center[0]) * 0.001

cv2.namedWindow("3D Cube")
cv2.setMouseCallback("3D Cube", mouse_callback)




