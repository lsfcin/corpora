import cv2
import mediapipe as mp
import pygetwindow as gw
import numpy as np
from pynput import mouse, keyboard
import threading
import matplotlib
import cv2
import torch
from ultralytics import YOLO
from depth_anything_v2.dpt import DepthAnythingV2

DEVICE = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'

depth_anything_configs = {
    'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
    'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
    'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
    'vitg': {'encoder': 'vitg', 'features': 384, 'out_channels': [1536, 1536, 1536, 1536]}
}

encoder = 'vits' # or 'vits', 'vitb', 'vitg'

# depth
depth_anything = DepthAnythingV2(**depth_anything_configs[encoder])
depth_anything.load_state_dict(torch.load(f'rsc/depth_anything_v2_{encoder}.pth', map_location='cpu'))
depth_anything = depth_anything.to(DEVICE).eval()

######################

# Load the YOLOv5 model
segmentation_yolo = YOLO(f'C:/Users/Lucas/Desktop/Workspace/Corpora/rsc/yolo11s-seg.pt')
def draw_segmentation(image, masks, boxes, labels, scores, threshold=0.5):
    for mask, box, label, score in zip(masks, boxes, labels, scores):
        if score >= threshold:
            color = (240, 240, 0)
            mask = mask.cpu().numpy()
            mask = (mask > 0.5).astype(np.uint8)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(image, contours, -1, color, 2)
            x1, y1, x2, y2 = box
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(image, f"{label}: {score:.2f}", (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

######################

#raw_img = cv2.imread('your/image/path')
mouse_x = 0
mouse_y = 0

# Define callback functions for mouse events
def on_move(x, y):
    mouse_x = x
    mouse_y = y
    #print(f"Mouse moved to ({x}, {y})")

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y}) with {button}")
    else:
        print(f"Mouse released at ({x}, {y}) with {button}")

def on_scroll(x, y, dx, dy):
    print(f"Mouse scrolled at ({x}, {y}) with delta ({dx}, {dy})")

# Define callback functions for keyboard events
def on_press(key):
    try:
        print(f"Key pressed: {key.char}")
    except AttributeError:
        print(f"Special key pressed: {key}")

def on_release(key):
    print(f"Key released: {key}")
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Start mouse listener in a separate thread
mouse_listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)
mouse_thread = threading.Thread(target=mouse_listener.start)
mouse_thread.daemon = True
mouse_thread.start()

# Start keyboard listener in a separate thread
keyboard_listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
keyboard_thread = threading.Thread(target=keyboard_listener.start)
keyboard_thread.daemon = True
keyboard_thread.start()

# Initialize MediaPipe Face Mesh modules
mp_face_mesh = mp.solutions.face_mesh
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Set up the face mesh module
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

pose = mp_pose.Pose()

# Set up video capture from webcam
cap = cv2.VideoCapture(0)
active_window = gw.getActiveWindow()

cmap = matplotlib.colormaps.get_cmap('Spectral_r')

while cap.isOpened():

    success, image = cap.read()
    
    ############################

    depth = depth_anything.infer_image(image) # HxW raw depth map in numpy
    depth = (depth - depth.min()) / (depth.max() - depth.min()) * 255.0
    depth = depth.astype(np.uint8)
    depth = (cmap(depth)[:, :, :3] * 255)[:, :, ::-1].astype(np.uint8)
    
    cv2.imshow('Depth', depth)

    ############################

   # Perform object segmentation
    results = segmentation_yolo(image)
    masks = results[0].masks.data
    boxes = results[0].boxes.xyxy.cpu().numpy()
    labels = [segmentation_yolo.names[int(cls)] for cls in results[0].boxes.cls]
    scores = results[0].boxes.conf.cpu().numpy()

    # Draw the segmentation results on the frame
    draw_segmentation(image, masks, boxes, labels, scores)

    # Display the resulting frame
    #cv2.imshow('Object Segmentation', image)
    
    
    ############################

    # Get the active window
    current_window = gw.getActiveWindow()

    # Print the title of the active window
    if active_window.title != current_window.title:
        active_window = current_window
        print(f"Current focused window name: {active_window.title}")

    
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Convert the image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and get face landmarks
    face_results = face_mesh.process(image_rgb)
    
    # Process the image and find body landmarks
    pose_results = pose.process(image_rgb)

    # Draw the face mesh on the image
    if face_results.multi_face_landmarks:        
        for face_landmarks in face_results.multi_face_landmarks:
            # Draw landmarks and connections
            mp_drawing.draw_landmarks(
                image,
                face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,  # Draw connections
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1)
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
        if pose_results.pose_landmarks:
            # Draw the pose landmarks
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=pose_results.pose_landmarks,
                connections=mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2)
            )
            
    # Display the resulting image
    cv2.imshow('Face Mesh', image)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
