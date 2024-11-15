import src.hpe as hpe
import src.depth as depth

import cv2
import mediapipe as mp
import pygetwindow as gw
import numpy as np
from pynput import mouse, keyboard
import threading
import matplotlib
import torch
from ultralytics import YOLO
from depth_anything_v2.dpt import DepthAnythingV2

DEVICE = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'

pose = hpe.PoseEstimator()
depth = depth.DepthEstimator()

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

# Set up video capture from webcam
cap = cv2.VideoCapture(0)
active_window = gw.getActiveWindow()

# cmap = matplotlib.colormaps.get_cmap('Spectral_r')

while cap.isOpened():

    success, image = cap.read()
    
    depth.process(image)
    depth_map = depth.draw(image)
    cv2.imshow('Depth', depth_map)

   # Perform object segmentation
    results = segmentation_yolo(image)
    masks = results[0].masks.data
    boxes = results[0].boxes.xyxy.cpu().numpy()
    labels = [segmentation_yolo.names[int(cls)] for cls in results[0].boxes.cls]
    scores = results[0].boxes.conf.cpu().numpy()

    # Draw the segmentation results on the frame
    draw_segmentation(image, masks, boxes, labels, scores)  
    
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

    pose.process(image_rgb)
    pose.draw(image)

    # Display the resulting image
    cv2.imshow('Face Mesh', image)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
