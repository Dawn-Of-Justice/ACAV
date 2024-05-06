import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox

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

    def is_bbox_inside(bbox1, bbox2):
        """
        Check if bbox1 is completely inside bbox2.

        Parameters:
            bbox1 (tuple): Coordinates of the first bounding box in the format (x1, y1, x2, y2).
            bbox2 (tuple): Coordinates of the second bounding box in the format (x1, y1, x2, y2).

        Returns:
            bool: True if bbox1 is completely inside bbox2, False otherwise.
        """
        x1, y1, x2, y2 = bbox1
        x1_inside = bbox2[0] <= x1 <= bbox2[2]
        y1_inside = bbox2[1] <= y1 <= bbox2[3]
        x2_inside = bbox2[0] <= x2 <= bbox2[2]
        y2_inside = bbox2[1] <= y2 <= bbox2[3]

        return x1_inside and y1_inside and x2_inside and y2_inside

if __name__ == "__main__":
    
    detector = objDet()
    img = cv2.imread(r"C:\Users\salos\OneDrive\Desktop\images.jpeg")
    bbox, label, conf = detector.detect(img, return_bbox=True)
    
    detector.draw_bbox(img, bbox, label, conf)
    
    print(label, conf)

    cv2.imshow('image', img)
    cv2.waitKey(0)