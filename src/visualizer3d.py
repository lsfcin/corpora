import cv2
import numpy as np

# Define the 3D points of a cube
cube_points = np.array([
    [-1, -1, -1],
    [-1, -1,  1],
    [-1,  1, -1],
    [-1,  1,  1],
    [ 1, -1, -1],
    [ 1, -1,  1],
    [ 1,  1, -1],
    [ 1,  1,  1]
], dtype=np.float32)

# Define edges of the cube (pairs of indices)
cube_edges = [
    (0, 1), (1, 3), (3, 2), (2, 0),  # Back face
    (4, 5), (5, 7), (7, 6), (6, 4),  # Front face
    (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting edges
]

# Camera settings
focal_length = 500
center = (300, 300)
camera_matrix = np.array([
    [focal_length, 0, center[0]],
    [0, focal_length, center[1]],
    [0, 0, 1]
], dtype=np.float32)

# Rotation and translation
rotation_vector = np.zeros((3, 1), dtype=np.float32)  # No initial rotation
translation_vector = np.array([[0], [0], [5]], dtype=np.float32)  # Translate away from the camera

# Mouse interaction
angle_x, angle_y = 0.0, 0.0  # Ensure these are floats

def mouse_callback(event, x, y, flags, param):
    global angle_x, angle_y
    if event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        angle_x += (y - center[1]) * 0.001
        angle_y += (x - center[0]) * 0.001

cv2.namedWindow("3D Cube")
cv2.setMouseCallback("3D Cube", mouse_callback)

while True:
    # Convert angles to np.float32 for consistency
    rotation_matrix_x = cv2.Rodrigues(np.array([angle_x, 0, 0], dtype=np.float32))[0]
    rotation_matrix_y = cv2.Rodrigues(np.array([0, angle_y, 0], dtype=np.float32))[0]
    rotation_matrix = rotation_matrix_y @ rotation_matrix_x
    rotation_vector, _ = cv2.Rodrigues(rotation_matrix)

    # Project 3D points to 2D
    projected_points, _ = cv2.projectPoints(cube_points, rotation_vector, translation_vector, camera_matrix, None)
    projected_points = projected_points.reshape(-1, 2)

    # Create blank image
    img = np.zeros((600, 600, 3), dtype=np.uint8)

    # Draw edges
    for edge in cube_edges:
        pt1 = tuple(projected_points[edge[0]].astype(int))
        pt2 = tuple(projected_points[edge[1]].astype(int))
        cv2.line(img, pt1, pt2, (0, 255, 0), 2)

    # Show the image
    cv2.imshow("3D Cube", img)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

