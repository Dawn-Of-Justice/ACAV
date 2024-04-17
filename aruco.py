import cv2
import mediapipe as mp

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize MediaPipe Pose module for hand landmarks
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Function to check hand posture
def check_hand_posture(hand_landmarks):
    # Implement your logic here to determine hand posture
    # For example, you can check for thumbs up or hi gesture
    
    # Placeholder logic, replace with actual detection algorithm
    return "thumbs_up"  # Replace with appropriate gesture

# Function to call when thumbs up is detected
def thumbs_up_action():
    # Implement your action when thumbs up is detected
    print("Thumbs up detected! Calling function...")

# Function to call when hi gesture is detected
def hi_action():
    # Implement your action when hi gesture is detected
    print("Hi gesture detected! Calling function...")

# Main function for ArUco marker detection and hand posture recognition
def detect_aruco_and_hand_posture(image):
    # Convert image to grayscale for ArUco marker detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # ArUco marker detection
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters_create()
    corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # If ArUco marker(s) detected
    if ids is not None:
        # Iterate through detected markers
        for i in range(len(ids)):
            # Process each marker individually
            marker_id = ids[i][0]
            marker_corners = corners[i][0]

            # Draw ArUco marker
            cv2.aruco.drawDetectedMarkers(image, corners)

            # Additional processing based on marker ID if needed
            # For example, if marker_id == 1, perform hand posture recognition
            if marker_id == 1:
                # Hand posture recognition
                results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        hand_posture = check_hand_posture(hand_landmarks)
                        if hand_posture == "thumbs_up":
                            thumbs_up_action()
                        elif hand_posture == "hi":
                            hi_action()

    return image

# Main function to capture video stream and detect ArUco marker and hand posture
def main():
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect ArUco marker and hand posture
        frame = detect_aruco_and_hand_posture(frame)

        cv2.imshow('ArUco Marker and Hand Posture Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
