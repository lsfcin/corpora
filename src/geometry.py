import cv2
import box
import numpy as np

class Geometry:
    def __init__(self):
        self.boxes = []
        pass

    def create_bounding_box(self, top_left_front, bottom_right_back, label):
        scale = np.abs(top_left_front - bottom_right_back)
        center = (top_left_front + bottom_right_back) / 2
        bounding_box = box.Box(center, scale, label)
        return bounding_box

        # Create 8 points of the bounding box
        # points = [
        #     top_left_front,
        #     [bottom_right_back[0], top_left_front[1], top_left_front[2]],
        #     [top_left_front[0], bottom_right_back[1], top_left_front[2]],
        #     [top_left_front[0], top_left_front[1], bottom_right_back[2]],
        #     [bottom_right_back[0], bottom_right_back[1], top_left_front[2]],
        #     [bottom_right_back[0], top_left_front[1], bottom_right_back[2]],
        #     [top_left_front[0], bottom_right_back[1], bottom_right_back[2]],
        #     bottom_right_back
        # ]

        # # Create lines connecting the points
        # lines = [
        #     [0, 1], 
        #     [0, 2], 
        #     [0, 3],
        #     [1, 4], 
        #     [1, 5],
        #     [2, 4], 
        #     [2, 6],
        #     [3, 5], 
        #     [3, 6],
        #     [4, 7],
        #     [5, 7],
        #     [6, 7]
        # ]

        # colors = [color for _ in range(len(lines))]

        #return [points, lines, colors]
    
    

    # receive a depth map and a segmentation mask and 
    # return the 3D boundung boxes and orientations of the objects
    def process(self, depth_map, contours, labels):

        # Clear the list of 3D bounding boxes and orientations
        self.boxes.clear()

        # List to store the 3D bounding boxes and orientations
        for contour, label in zip(contours, labels):

            # Find the maximum and the average depth values of the object in the current contour        
            # Create a mask for the current contour
            contour_mask = np.zeros_like(depth_map, dtype=np.uint8)
            cv2.drawContours(contour_mask, [contour], -1, 255, thickness=cv2.FILLED)

            # Extract the depth values within the contour
            depth_values = depth_map[contour_mask == 255]

            # Calculate the minimum, maximum, and average depth values
            max_depth = np.max(depth_values)
            avg_depth = np.mean(depth_values)

            # Calculate the 2D bounding box
            x, y, w, h = cv2.boundingRect(contour)

            # Extract the depth values for the bounding box corners
            depth_front = max_depth  # Top-left corner
            depth_back = avg_depth - (max_depth - avg_depth)  # Top-right corner

            # Estimate the 3D coordinates of the bounding box corners
            top_left_front = np.array([x, y, depth_front])
            bottom_right_back = np.array([x + w, y + h, depth_back])

            # Store the 3D bounding box and orientation
            box = self.create_bounding_box(top_left_front, bottom_right_back, label)
            self.boxes.append(box)

    def project_point(self, point, camera_matrix, rotation_vector, translation_vector):
        # Project the 3D point to the 2D image plane
        point = point.reshape(1, 3)
        image_points, _ = cv2.projectPoints(point, rotation_vector, translation_vector, camera_matrix, None)
        return image_points[0][0]

    # def show(self):

    #     # Create an opencv window
    #     cv2.namedWindow('Geometry', cv2.WINDOW_NORMAL)

    #     # Create a blank image
    #     image = np.zeros((720, 1280, 3), dtype=np.uint8)

    #     # Draw the 3D bounding boxes
    #     self.draw_3D_bounding_boxes(image)

    #     # Display the image
    #     cv2.imshow('Geometry', image)

    # def draw_3D_bounding_boxes(self, image):
    #     for box in self.boxes_3d:
    #         # Create the 3D bounding box
    #         cube = self.create_box(box)

    #         # Project the 3D bounding box to the 2D image plane
    #         projected_points = []
    #         for point in cube.points:
    #             projected_point = self.project_point(point, self.camera_matrix, self.rotation_vector, self.translation_vector)
    #             projected_points.append(projected_point)

    #         # Draw the 3D bounding box
    #         for edge in cube.edges:
    #             cv2.line(image, projected_points[edge[0]], projected_points[edge[1]], (0, 255, 0), 2)

# # Create an Open3D LineSet object
# line_set = o3d.geometry.LineSet()
# line_set.points = o3d.utility.Vector3dVector(points)
# line_set.lines = o3d.utility.Vector2iVector(lines)
# line_set.colors = o3d.utility.Vector3dVector([[0, 1, 0] for _ in range(len(lines))])  # Green color
