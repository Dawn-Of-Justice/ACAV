import cv2

class ArUcoDetector:
    def __init__(self):
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.aruco_params = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.aruco_params)

    def detect_markers(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = self.detector.detectMarkers(gray)
        if corners is not None and ids is not None:
            for corner, id in zip(corners, ids):
                x, y, w, h = cv2.boundingRect(corner)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"ArUco Marker {id[0]}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            return frame, [(id[0], corner) for id, corner in zip(ids, corners)]
        return None, None

if __name__ == "__main__":
    detector = ArUcoDetector()
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
        result, ids_with_corners = detector.detect_markers(frame)
        if result is not None:
            cv2.imshow('Frame', result)
            if ids_with_corners:
                for id, corner in ids_with_corners:
                    cv2.putText(result, f"ArUco Marker {id}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        else:
            cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    detector = ArUcoDetector()
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
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