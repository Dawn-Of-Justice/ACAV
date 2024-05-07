from server import VideoReceiver
from aruco import ArUcoDetector
from datacollector import Preprocessor
from gesture import ProtectionSystem
from obj_det import objDet
import cv2
import numpy as np
import threading

receiver = VideoReceiver()
receiver.accept_connection()
detector = ArUcoDetector()
processor = Preprocessor()
protection_system = ProtectionSystem("code/server-pc/keras_Model.h5", "code/server-pc/labels.txt")
ObjectDetect = objDet()

def get_command(command):
    receiver.send_command(command)

# command_thread = threading.Thread(target=get_command)
# command_thread.daemon = True
# command_thread.start()

while True:

    frame = receiver.receive_frame()
    if frame is None:
        continue
    if not receiver.display_frame(frame):
        break
    result, ids_with_corners = detector.detect_markers(frame)
    if result is not None:
        # cv2.imshow('Frame', result)
        if ids_with_corners:
            bboxes, classes, _ = ObjectDetect.detect(frame, return_bbox=True)
            aruco_id = ids_with_corners[0][1][0][0][0],ids_with_corners[0][1][0][0][1],ids_with_corners[0][1][0][2][0],ids_with_corners[0][1][0][2][1]
            if 'person' in classes:
                idx = classes.index('person')
                bbox = bboxes[idx]
                # print('aruco',aruco_id)
                # print('person:',bbox)
            if objDet.is_bbox_inside(aruco_id, bbox):
                # print('Aruco Inside')
                try:
                    image = cv2.resize(frame,(640, 430))
                    masked_image = processor.process(image)

                    if masked_image is not None:
                        cv2.imshow('Skelton', masked_image)

                    class_name, confidence_score = protection_system.predict(masked_image)
                    print("Class:", class_name[2:], end="")
                    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

                except Exception as e:
                    pass

        cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
receiver.close_connection()