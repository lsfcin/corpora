import src.hpe as hpe
import src.depth as depth
import src.segment as segment

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

pose = hpe.PoseEstimator()
depth = depth.DepthEstimator()
segment = segment.Segmenter()

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

while cap.isOpened():

    success, frame = cap.read()
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    depth_map = frame.copy()

    pose.process(image_rgb)
    depth.process(frame)
    segment.process(frame)
    
    pose.draw(frame)
    depth.draw(depth_map)
    segment.draw(frame)  
    

    # Get the active window
    current_window = gw.getActiveWindow()

    # Print the title of the active window
    if active_window.title != current_window.title:
        active_window = current_window
        print(f"Current focused window name: {active_window.title}")

    
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Display the resulting image
    cv2.imshow('Depth', depth_map)
    cv2.imshow('Face Mesh', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
