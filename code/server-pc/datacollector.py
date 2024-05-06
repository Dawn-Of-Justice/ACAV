import mediapipe as mp
import cv2
import numpy as np
import os
import json
from tqdm import tqdm
from server import VideoReceiver
from PIL import Image
from obj_det import objDet

class Preprocessor():

    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_pose = mp.solutions.pose
        self.mp_pose = mp.solutions.pose.Pose()
        self.mp_hands = mp.solutions.hands.Hands()
        self.obj_det = objDet()

    def detect_hands(self,image, size = (640, 430)):
        blank_image = np.zeros(shape=(430, 640, 3))
        results_hands = self.mp_hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        # Draw hand landmarks and connections
        if results_hands.multi_hand_landmarks:
            for hand_landmarks in results_hands.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    blank_image,
                    hand_landmarks,
                    mp.solutions.hands.HAND_CONNECTIONS
        )
        return blank_image

    def process(self, image):
        bboxes, classes, _ = self.obj_det.detect(image, return_bbox=True)
        if 'person' in classes:
            idx = classes.index('person')
            bbox = bboxes[idx]
            # cv2.rectangle(blank_image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color=(0,255,0), thickness=5)
            pil_image = Image.fromarray(image)
            cropped_image = pil_image.crop(bbox)
            # cv2.imshow("cropped",image[bbox[0]:bbox[1], bbox[2]:bbox[3]])
            # cv2.imshow("cropped",np.array(cropped_image))
            cropped_image = np.array(cropped_image)
            cropped_image_blank = self.detect_hands(cropped_image)
            return cropped_image_blank

if __name__ == "__main__":

    # image = cv2.imread(r"C:\Users\salos\OneDrive\Desktop\hi.jpg")
    # masked_image = processor.process(image)
    # cv2.imshow("img", masked_image)
    # cv2.waitKey(0)

    processor = Preprocessor()
    receiver = VideoReceiver()
    receiver.accept_connection()

    blank_num = 0
    go_num = 0
    stop_num = 0

    while True:
        frame = receiver.receive_frame()
        if frame is None:
            continue

        image = cv2.resize(frame,(640, 430))
        masked_image = processor.process(image)

        if masked_image is not None:
            cv2.imshow('Skelton', masked_image)

        key = cv2.waitKey(1) 

        if key == ord("b"):
            print('hi')
            if masked_image is not None :
                cv2.imwrite(r'C:\Users\salos\OneDrive\Documents\GitHub\ACAV\code\Data\Blank\image_{}.jpg'.format(blank_num), masked_image)
                blank_num += 1

        if key == ord("s"):
            print('stop')
            if masked_image is not None :
                cv2.imwrite(r'C:\Users\salos\OneDrive\Documents\GitHub\ACAV\code\Data\Stop\image_{}.jpg'.format(stop_num), masked_image)
                stop_num += 1

        if key == ord("g"):
            print('go')
            if masked_image is not None:
                cv2.imwrite(r'C:\Users\salos\OneDrive\Documents\GitHub\ACAV\code\Data\Go\image_{}.jpg'.format(go_num), masked_image)
                go_num += 1

        if key == ord("q"):
            break

        if not receiver.display_frame(frame):
            break
    receiver.close_connection()