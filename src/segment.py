# Segmenter: YOLO11-seg instance segmentation wrapper producing masks and bounding boxes
import cv2
import numpy as np
from ultralytics import YOLO

class Segmenter:
    def __init__(self):
        self.segmenter = YOLO(f'rsc/yolo11s-seg.pt')
        self.results = None
        self.masks = None
        self.boxes = None
        self.labels = None
        self.scores = None
        self.contours = None
    
    def show(self, image, threshold=0.5):
        for mask, box, label, score in zip(self.masks, self.boxes, self.labels, self.scores):
            if score >= threshold:
                color = (240, 0, 220)
                cv2.drawContours(image, self.contours, -1, color, 2)
                x1, y1, x2, y2 = box
                cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                cv2.putText(image, f"{label}: {score:.2f}", (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def process(self, image):
        self.results = self.segmenter.predict(image)
        self.masks = self.results[0].masks.data
        self.boxes = self.results[0].boxes.xyxy.cpu().numpy()
        self.labels = [self.segmenter.names[int(cls)] for cls in self.results[0].boxes.cls]
        self.scores = self.results[0].boxes.conf.cpu().numpy()
        for mask in self.masks:
            mask = mask.cpu().numpy()
            mask = (mask > 0.5).astype(np.uint8)
            self.contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    def get(self):
        return self.masks, self.boxes, self.labels, self.scores, self.contours
        