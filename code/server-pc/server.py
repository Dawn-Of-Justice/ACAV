import cv2
import socket
import numpy as np

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
        if frame is None:
            #print("Error decoding image. Data length:", len(jpg))
            return None
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

if __name__ == '__main__':
    main()