import mediapipe as mp
import cv2
import numpy as np
import os
import json
from tqdm import tqdm
from server import VideoReceiver
from PIL import Image

from cvlib import object_detection

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

mp_pose = mp.solutions.pose.Pose()
    
# Initialize MediaPipe Hands model
mp_hands = mp.solutions.hands.Hands()


class Preprocessor():

    def __init__(self):

        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_pose = mp.solutions.pose

        mp_pose = mp.solutions.pose.Pose()
            
        # Initialize MediaPipe Hands model
        mp_hands = mp.solutions.hands.Hands()




    def detect_hands(self,image, size = (640, 430)):

        blank_image = np.zeros(shape=(430, 640, 3))
        results_hands = mp_hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

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

        bboxes, classes, scores = object_detection.detect_common_objects(image, enable_gpu=True)

        if 'person' in classes:
            idx = classes.index('person')
            bbox = bboxes[idx]
            # cv2.rectangle(blank_image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color=(0,255,0), thickness=5)

            pil_image = Image.fromarray(image)
            cropped_image = pil_image.crop(bbox)
            # cv2.imshow("cropped",image[bbox[0]:bbox[1], bbox[2]:bbox[3]])
            # cv2.imshow("cropped",np.array(cropped_image))
            cropped_image_blank = self.detect_hands(np.array(cropped_image))


        return cropped_image_blank



if __name__ == "__main__":


    image = cv2.imread(r"C:\Users\ROHIT FRANCIS\Downloads\Person_Thumbs_Up.jpeg")


    processor = Preprocessor()

    cropped_image = processor.process(image)

    cv2.imshow("data", cropped_image)
    cv2.waitKey(0)
    # receiver = VideoReceiver()
    # receiver.accept_connection()
    # while True:
    #     frame = receiver.receive_frame()
    #     if frame is None:
    #         continue

    #     image = cv2.resize(frame,(640, 430))

    #     #output will be like ([[182, -6, 644, 486]], ['person'], [0.8795058727264404])
    #     bboxes, classes, scores = object_detection.detect_common_objects(frame, enable_gpu=True)
        

    #     if 'person' in classes:
    #         idx = classes.index('person')
    #         bbox = bboxes[idx]
    #         # cv2.rectangle(blank_image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color=(0,255,0), thickness=5)

    #         pil_image = Image.fromarray(image)
    #         cropped_image = pil_image.crop(bbox)
    #         # cv2.imshow("cropped",image[bbox[0]:bbox[1], bbox[2]:bbox[3]])
    #         cv2.imshow("cropped",np.array(cropped_image))
    #         blank_image = processor.detect_hands(image)

    #     if cv2.waitKey(1) == ord("q"):
    #         break

    #     # cv2.imshow('MediaPipe Pose', blank_image)

    #     if not receiver.display_frame(frame):
    #         break
    # receiver.close_connection()