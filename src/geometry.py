import cv2
import numpy as np
import open3d as o3d
import src.box as box

class Geometry:
    def __init__(self):
        self.boxes = []
        self.frame_id = 0
        
        # Create a visualization object and window
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()

    def create_box(self, top_left_front, bottom_right_back, label):
        scale = np.abs(top_left_front - bottom_right_back)
        center = (top_left_front + bottom_right_back) / 2
        bounding_box = box.Box(center, scale, label)
        return bounding_box

    # Receive a depth map and a segmentation mask and 
    # Updates the 3D boundung boxes and orientations of the objects
    def process(self, depth_map, contours, labels):
        self.frame_id += 1

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
            box = self.create_box(top_left_front, bottom_right_back, label, self.frame_id)
            self.track(box)

    def track(self, box):
        found = False

        dimensions_threshold = 0.3
        centers_threshold = 0.3

        # Attempt to find (Re-ID) the box in the list of boxes
        # First filter the boxes that have the same label
        for i, b in enumerate(self.boxes):
            if b.label == box.label:
                # Then check if the dimensions are similar
                similar_dimensions = np.linalg.norm(b.dimensions - box.dimensions) < dimensions_threshold

                # And check if the distance between the centers falls within a threshold based on the dimensions
                nearby_centers = np.linalg.norm(b.center - box.center) < np.linalg.norm(box.dimensions) * centers_threshold
                
                if similar_dimensions and nearby_centers:
                    found = True
                    id = i
                    break

        if found:
            self.boxes[id].update(box, self.frame_id)
        else:
            self.vis.add_geometry(box.line_set)
            self.boxes.append(box)
    
    def show(self):
        
        for box in self.boxes:
            self.vis.update_geometry(box.line_set)
        
        self.vis.poll_events()
        self.vis.update_renderer()

    # def project_point(self, point, camera_matrix, rotation_vector, translation_vector):
    #     # Project the 3D point to the 2D image plane
    #     point = point.reshape(1, 3)
    #     image_points, _ = cv2.projectPoints(point, rotation_vector, translation_vector, camera_matrix, None)
    #     return image_points[0][0]

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
