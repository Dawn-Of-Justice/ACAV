import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import pandas as pd


class objDet:
    def __init__(self, model="yolov4", confidence=0.5):
        self.model = model
        self.confidence = confidence

    def detect(self,image, return_bbox=False):
        bbox, label, conf = cv.detect_common_objects(image, confidence=self.confidence, model=self.model)

        if return_bbox:
            return bbox, label, conf
        else:
            return label, conf
    def draw_bbox(self,image,bboxes, labels, confidence):
        cv.object_detection.draw_bbox(image,bboxes, labels, confidence)


if __name__ == "__main__":
    
    detector = objDet()
    img = cv2.imread(r"C:\Users\salos\OneDrive\Desktop\images.jpeg")
    bbox, label, conf = detector.detect(img, return_bbox=True)
    
    
    detector.draw_bbox(img, bbox, label, conf)
    
    print(label, conf)

    cv2.imshow('image', img)
    cv2.waitKey(0)