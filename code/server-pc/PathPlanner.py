import random
import cv2
from cvlib import object_detection

class PathPlanning:

    def __init__(self, centre_of_tracking:tuple):
        

        self.lane_1 = centre_of_tracking[0]
        self.lane_2 = centre_of_tracking[1]
        self.track = None
        self.centre_of_tracking = centre_of_tracking
        self.l_or_r = None
        self.reset = False

    def lane_assist(self, current_x:int, current_y:int):
        
        self.track = (current_x, current_y)

        if self.centre_of_tracking[0] < self.track[0]:
            return 'r'
        
        if self.centre_of_tracking[0] > self.track[0]:
            return 'l'

        if self.reset == True:
            self.l_or_r = None
            self.reset = False

    def correct_path(self, obstacle_endpoints:tuple, reset=False):

        # Turn until one of the assisting lanes gets corrected:
        if self.l_or_r ==  None:
            self.l_or_r =  random.choice(["left", "right"])

        return self.l_or_r
    

import cv2
import socket
import numpy as np

pathplanner = PathPlanning((300, 400))

class VideoReceiver:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("0.0.0.0", 5000))
        self.sock.listen(1)
        print("Waiting for connection...")

    def accept_connection(self):
        self.conn, self.addr = self.sock.accept()
        print("Connected by", self.addr)

    def receive_frame(self):
        jpg = bytearray()
        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            jpg.extend(data)
            if b'END_OF_IMAGE' in jpg:  
                jpg = jpg[:-12]  
                break
        if len(jpg) == 0:
            print("No data received. Connection closed.")
            return None
        frame = cv2.imdecode(np.frombuffer(jpg, np.uint8), cv2.IMREAD_COLOR)
        
        # print(detected)
        
        if frame is None:
            #print("Error decoding image. Data length:", len(jpg))
            return None
        
        if frame is not None:

            pathplanner.lane_1 = int(frame.shape[0]*0.5)
            pathplanner.lane_2 = int(frame.shape[0]*0.9)
            pathplanner.centre_of_tracking = (pathplanner.lane_1, pathplanner.lane_2)

            detected = object_detection.detect_common_objects(frame,confidence=0.2)

            if detected[0]:
                # pathplanner.correct_path(obstacle_endpoints=(int((detected[0][0][0]+detected[0][0][1])/2), int((detected[0][0][2]+detected[0][0][3])/2)))
                pathplanner.lane_assist(int((detected[0][0][0]+detected[0][0][1])/2), int((detected[0][0][2]+detected[0][0][3])/2))

        return frame

    def display_frame(self, frame, Title='Received'):
        cv2.imshow(Title, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.conn.close()
            cv2.destroyAllWindows()
            return False
        return True

    def close_connection(self):
        self.conn.close()
        cv2.destroyAllWindows()

def main():
    receiver = VideoReceiver()
    receiver.accept_connection()
    while True:
        frame = receiver.receive_frame()
        if frame is None:
            continue
        if not receiver.display_frame(frame):
            break
    receiver.close_connection()

# if __name__ == '__main__':
#     main()



if __name__ == "__main__":
    # Testcode is ran here
    
    import cv2
    from cvlib import object_detection


    # obj_detector = object_detection.detect_common_objects()
    pathplanner = PathPlanning((300, 400))


    cam = cv2.VideoCapture(0)

    while True:

        ret, frame = cam.read()

        pathplanner.lane_1 = int(frame.shape[0]*0.5)
        pathplanner.lane_2 = int(frame.shape[0]*0.9)
        pathplanner.centre_of_tracking = (pathplanner.lane_1, pathplanner.lane_2)
        if cv2.waitKey(1) == ord("q"):
            break
        detected = object_detection.detect_common_objects(frame,confidence=0.5)
        if detected:
            # print(detected)
            object_detection.draw_bbox(frame,detected[0],detected[1],detected[2])
            # print(detected[0][0][0], detected[0][0][1], detected[0][0][2], detected[0][0][3])

            # print((detected[0][0][0]+detected[0][0][1])/2, (detected[0][0][2]+detected[0][0][3])/2)


            cv2.circle(frame, center=(int((detected[0][0][0]+detected[0][0][1])/2), int((detected[0][0][2]+detected[0][0][3])/2)), thickness=3, color=(0,0,0), radius=3)

            cv2.line(frame, (pathplanner.lane_1,200), (pathplanner.lane_1, 400), (0,255,0), 2)
            cv2.line(frame, (pathplanner.lane_2,200), (pathplanner.lane_2, 400), (0,255,0), 2)
        cv2.imshow("feed", frame)

    cam.release()
    cv2.destroyAllWindows()


