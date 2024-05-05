from server import VideoReceiver
from aruco import ArUcoDetector
import cv2

receiver = VideoReceiver()
receiver.accept_connection()
detector = ArUcoDetector()

while True:
    frame = receiver.receive_frame()
    if frame is None:
        continue
    if not receiver.display_frame(frame):
        break
    result, ids = detector.detect_markers(frame)
    if result is not None:
        cv2.imshow('Frame', result)
        if ids:
            cv2.putText(result, f"Detected ArUco Markers: {ids}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    else:
        cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
receiver.close_connection()