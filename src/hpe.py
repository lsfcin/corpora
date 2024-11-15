# hpe stands for human pose estimator

import cv2
import numpy as np
import mediapipe as mp

# Create pose class
class Pose:
    def __init__(self):
        # Initialize MediaPipe Face Mesh modules
        self.mp_body_pose = mp.solutions.pose
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        # Set up the face mesh module
        
        self.body_pose = self.mp_body_pose.Pose()
        
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)


    def process(self, image_rgb, print_elapsed_time=False):
        # Process the image and find body landmarks
        self.body_results = self.body_pose.process(image_rgb)

        # Process the image and get face landmarks
        self.face_results = self.face_mesh.process(image_rgb)

    def get(self):
        return self.body_results, self.face_results

    def draw(self, image):
        # Draw the face mesh on the image
        if self.face_results.multi_face_landmarks:        
            for face_landmarks in self.face_results.multi_face_landmarks:
                # Draw landmarks and connections
                self.mp_drawing.draw_landmarks(
                    image,
                    face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_TESSELATION,  # Draw connections
                    landmark_drawing_spec=self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                    connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1)
                )

                # Extract the coordinates of the left and right eye landmarks
                left_eye = face_landmarks.landmark[33]  # Example landmark for left eye
                right_eye = face_landmarks.landmark[263]  # Example landmark for right eye
                nose_tip = face_landmarks.landmark[1]  # Example landmark for nose tip
                mouth_left = face_landmarks.landmark[61]  # Example landmark for left mouth corner
                mouth_right = face_landmarks.landmark[291]  # Example landmark for right mouth corner
                left_iris = face_landmarks.landmark[468]  # Example landmark for left iris
                right_iris = face_landmarks.landmark[473]  # Example landmark for right iris

                # Calculate the midpoint between the eyes
                eye_center_x = (left_eye.x + right_eye.x) / 2
                eye_center_y = (left_eye.y + right_eye.y) / 2
                eye_center_z = (left_eye.z + right_eye.z) / 2

                # Calculate the center of the mouth
                mouth_center_x = (mouth_left.x + mouth_right.x) / 2
                mouth_center_y = (mouth_left.y + mouth_right.y) / 2
                mouth_center_z = (mouth_left.z + mouth_right.z) / 2

                # Calculate the vector between the user's eyes
                eye_vector = np.array([right_eye.x - left_eye.x, right_eye.y - left_eye.y, right_eye.z - left_eye.z])

                # Calculate the vector between the center of the eyes and the center of the mouth
                eye_to_mouth_vector = np.array([mouth_center_x - eye_center_x, mouth_center_y - eye_center_y, mouth_center_z - eye_center_z])

                # Calculate the cross product of the two vectors
                cross_product_vector = np.cross(eye_vector, eye_to_mouth_vector)

                # Increase the vector size by 5 times and negate it to point outward
                scaled_cross_product_vector = -cross_product_vector * 15

                # Convert normalized coordinates to pixel coordinates
                h, w, _ = image.shape
                nose_tip_coords = (int(nose_tip.x * w), int(nose_tip.y * h))
                cross_product_coords = (int((nose_tip.x + scaled_cross_product_vector[0]) * w), int((nose_tip.y + scaled_cross_product_vector[1]) * h))

                # Draw the cross product vector
                cv2.arrowedLine(image, nose_tip_coords, cross_product_coords, (0, 0, 255), 2)
                
                # Calculate the midpoint between the irises
                iris_center_x = (left_iris.x + right_iris.x) / 2
                iris_center_y = (left_iris.y + right_iris.y) / 2
                iris_center_z = (left_iris.z + right_iris.z) / 2

                # Calculate the vector from the center of the eyes to the iris center
                iris_vector = np.array([iris_center_x - eye_center_x, iris_center_y - eye_center_y, iris_center_z - eye_center_z])

                # Increase the vector size by 5 times
                scaled_iris_vector = iris_vector * 10

                # Convert normalized coordinates to pixel coordinates
                iris_vector_coords = (int((eye_center_x + scaled_iris_vector[0]) * w), int((eye_center_y + scaled_iris_vector[1]) * h))

                # Draw the iris direction vector
                eye_center_coords = (int(eye_center_x * w), int(eye_center_y * h))
                cv2.arrowedLine(image, eye_center_coords, iris_vector_coords, (0, 0, 255), 2)
                
            # Check if any body landmarks are detected
            if self.body_results.pose_landmarks:
                # Draw the pose landmarks
                self.mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=self.body_results.pose_landmarks,
                    connections=self.mp_body_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=self.mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2),
                    connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2)
                )