# hpe stands for human pose estimator

import cv2
import numpy as np
import mediapipe as mp

import src.pose6dof as pose6dof

# Create pose class
class PoseEstimator:
    def __init__(self):
        # Initialize MediaPipe Face Mesh modules
        self.mp_body_pose = mp.solutions.pose
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Set up the body pose module
        self.body_pose = self.mp_body_pose.Pose()
        
        # Set up the face mesh module
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
        
        # Set up the gaze and head module
        self.gaze = pose6dof.Pose6DOF(np.array([0, 0, 0]), np.array([0, 0, 0]))
        self.head = pose6dof.Pose6DOF(np.array([0, 0, 0]), np.array([0, 0, 0]))

    def process(self, image_rgb, print_elapsed_time=False):
        # Process the image and find body landmarks
        self.body_results = self.body_pose.process(image_rgb)

        # Process the image and get face landmarks
        self.face_results = self.face_mesh.process(image_rgb)

        # Extract the gaze and head pose
        self.extract_gaze_and_head(self.face_results)

    def get(self):
        return self.body_results, self.face_results

    def show(self, image):
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

                # Draw head pose
                h, w, _ = image.shape
                scaled_head_direction = -self.head.direction * 10
                head_position_2D = (int(self.head.position[0] * w), int(self.head.position[1] * h))
                head_direction_2D = (int((self.head.position[0] + scaled_head_direction[0]) * w), int((self.head.position[1] + scaled_head_direction[1]) * h))
                cv2.arrowedLine(image, head_position_2D, head_direction_2D, (0, 0, 255), 2)

                # Draw gaze
                scaled_gaze_vector = self.gaze.direction * 10
                gaze_direction_2D = (int((self.gaze.position[0] + scaled_gaze_vector[0]) * w), int((self.gaze.position[1] + scaled_gaze_vector[1]) * h))
                gaze_position_2D = (int(self.gaze.position[0] * w), int(self.gaze.position[1] * h))
                cv2.arrowedLine(image, gaze_position_2D, gaze_direction_2D, (0, 0, 255), 2)
                
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

    def extract_gaze_and_head(self, face_results):
        if self.face_results.multi_face_landmarks:        
            for face_landmarks in self.face_results.multi_face_landmarks:
                
                # Extract required landmarks
                left_eye = face_landmarks.landmark[33]
                right_eye = face_landmarks.landmark[263]
                nose_tip = face_landmarks.landmark[1]
                mouth_left = face_landmarks.landmark[61]
                mouth_right = face_landmarks.landmark[291]
                left_iris = face_landmarks.landmark[468]
                right_iris = face_landmarks.landmark[473]

                # Calculatations for head pose
                eye_center_x = (left_eye.x + right_eye.x) / 2
                eye_center_y = (left_eye.y + right_eye.y) / 2
                eye_center_z = (left_eye.z + right_eye.z) / 2
                
                mouth_center_x = (mouth_left.x + mouth_right.x) / 2
                mouth_center_y = (mouth_left.y + mouth_right.y) / 2
                mouth_center_z = (mouth_left.z + mouth_right.z) / 2

                eye_vector = np.array([right_eye.x - left_eye.x, right_eye.y - left_eye.y, right_eye.z - left_eye.z])
                eye_to_mouth_vector = np.array([mouth_center_x - eye_center_x, mouth_center_y - eye_center_y, mouth_center_z - eye_center_z])
                cross_product_vector = np.cross(eye_vector, eye_to_mouth_vector)

                self.head.position = np.array([nose_tip.x,nose_tip.y,nose_tip.z])
                self.head.direction = cross_product_vector
                
                # Calculatations for gaze pose
                iris_center_x = (left_iris.x + right_iris.x) / 2
                iris_center_y = (left_iris.y + right_iris.y) / 2
                iris_center_z = (left_iris.z + right_iris.z) / 2

                self.gaze.position = np.array([eye_center_x, eye_center_y, eye_center_z])
                self.gaze.direction = np.array([iris_center_x - eye_center_x, iris_center_y - eye_center_y, iris_center_z - eye_center_z])