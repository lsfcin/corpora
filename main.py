import src.hpe as hpe
import src.depth as depth
import src.segment as segment
import src.input as input
import src.window as window
import src.geometry as geometry
#import src.visualizer as visualizer

import cv2

pose = hpe.PoseEstimator()
depth = depth.DepthEstimator()
segment = segment.Segmenter()
input = input.Input()
window = window.Window()
geometry = geometry.Geometry()
#visualizer = visualizer.Visualizer()

# Set up video capture from webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():

    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    depth_map = frame.copy()

    pose.process(image_rgb)
    depth.process(frame)
    segment.process(frame)
    window.process()
    
    pose.show(frame)
    depth.show(depth_map)
    segment.show(frame)
    window.show()
    #visualizer.show()

    # Display the resulting image
    cv2.imshow('Depth', depth_map)
    cv2.imshow('Face Mesh', frame)

    # depth_map = depth.get()
    # masks,boxes,labels,scores,contours = segment.get()

    # geometry.process(depth_map, contours, labels)
    # geometry.show()

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
