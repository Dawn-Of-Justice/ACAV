import cv2
import socket
import numpy as np

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("0.0.0.0", 5000))
sock.listen(1)

print("Waiting for connection...")
conn, addr = sock.accept()
print("Connected by", addr)

while True:
    jpg = bytearray()
    while True:
        data = conn.recv(1024)
        if not data:
            break
        jpg.extend(data)
        if b'END_OF_IMAGE' in jpg:  # check for delimiter
            jpg = jpg[:-12]  # remove delimiter
            break
    if len(jpg) == 0:
        print("No data received. Connection closed.")
        break
    frame = cv2.imdecode(np.frombuffer(jpg, np.uint8), cv2.IMREAD_COLOR)
    if frame is None:
        print("Error decoding image.")
        break
    cv2.imshow('Received', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

conn.close()
cv2.destroyAllWindows()