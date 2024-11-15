import src.hpe as hpe
import src.depth as depth
import src.segment as segment
import src.input as input

import cv2
import pygetwindow as gw

pose = hpe.PoseEstimator()
depth = depth.DepthEstimator()
segment = segment.Segmenter()
input = input.Input()

input.start()

# Set up video capture from webcam
cap = cv2.VideoCapture(0)
active_window = gw.getActiveWindow()

while cap.isOpened():

    success, frame = cap.read()
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    depth_map = frame.copy()

    pose.process(image_rgb)
    depth.process(frame)
    #segment.process(frame)
    
    pose.draw(frame)
    depth.draw(depth_map)
    #segment.draw(frame)  

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
