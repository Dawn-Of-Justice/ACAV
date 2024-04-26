import server
import cv2

receiver = server.VideoReceiver()
receiver.accept_connection()
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
aruco_params = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

while True:
    frame = receiver.receive_frame()
    if frame is None:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = detector.detectMarkers(gray)
    if corners is not None and ids is not None:
        for corner, id in zip(corners, ids):
            x, y, w, h = cv2.boundingRect(corner)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"ArUco Marker {id[0]}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    if not receiver.display_frame(frame, 'ArUco Marker Detection'):
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

receiver.close_connection()
cv2.destroyAllWindows()