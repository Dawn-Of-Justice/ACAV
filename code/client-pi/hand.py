import cv2
import numpy as np

# Set up the camera
cap = cv2.VideoCapture(0)

# Set up the background subtractor
backSub = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = cap.read()
    
    # Apply background subtraction
    fgMask = backSub.apply(frame)
    
    # Convert to YCrCb color space
    ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    
    # Skin tone detection
    skin_mask = cv2.inRange(ycrcb, np.array([0, 133, 77]), np.array([255, 173, 127]))
    
    # Apply skin tone mask to the foreground mask
    skin_fgMask = cv2.bitwise_and(fgMask, fgMask, mask=skin_mask)
    
    # Find contours of the hand
    contours, _ = cv2.findContours(skin_fgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Analyze the contour shape and size
        if area > 1000 and area < 5000:
            contour_shape = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            if len(contour_shape) > 5:
                cv2.circle(frame, (x+w//2, y+h//2), 10, (0, 0, 255), -1)
    
    cv2.imshow('Hand Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()