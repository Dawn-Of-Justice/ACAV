import cv2
import socket
import sys
import time
import threading
from adafruit_motor import servo as servo_module
from adafruit_pca9685 import PCA9685
import RPi.GPIO as GPIO
import time
import board

# Set the pin numbering scheme
#GPIO.setmode(GPIO.BOARD)

print(GPIO.getmode())

# Set the pin number you want to control
pin_number =24

# Set the pin as an output
GPIO.setup(pin_number, GPIO.OUT)



def set_servo_angle(servo_number, angle):
    if servo_number < 16:
        if servo_number == 3:
            angle = 180 - angle 
        if angle > 180:
            angle = angle % 180
        i2c = board.I2C()
        pca = PCA9685(i2c)
        pca.frequency = 50
        if servo_number == 0 or servo_number == 1:
            servo_module.Servo(pca.channels[1-servo_number]).angle = (180-angle)
        servo_module.Servo(pca.channels[servo_number]).angle = angle
        pca.deinit()
    else:
        print("Error: Servo number must be under 16")


def receive_commands(sock):
    while True:
        try:
            command = sock.recv(1024).decode('utf-8')
            if command:
                print(f"Received command: {command}", type(command))
                # print(len(command.strip()), len(command))
                # print(command=='f')
                if command.strip() == "f":
                  print('hi')
                  GPIO.output(pin_number, GPIO.HIGH)
                elif command.strip() == 's':
                    GPIO.output(pin_number, GPIO.LOW)
                elif command.strip() == 'l':
                    set_servo_angle(0, 50)
                    time.sleep(1)
                    set_servo_angle(0, 90)
                elif command.strip() == 'r':
                    set_servo_angle(0, 140)
                    time.sleep(1)
                    set_servo_angle(0, 90)

                # For example, you can execute a shell command using os.system()
                # os.system(command)
            else:
                print("Connection lost. Reconnecting...")
                break
        except ConnectionResetError:
            print("Connection reset. Reconnecting...")
            break

def send_video(ip_address):
    cap = cv2.VideoCapture(-1)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            sock.connect((ip_address, 5000))
            break
        except ConnectionRefusedError:
            print("Connection refused. Retrying in 1 second...")
            time.sleep(1)

    # Create a separate thread for receiving commands
    command_thread = threading.Thread(target=receive_commands, args=(sock,))
    command_thread.daemon = True
    command_thread.start()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        _, jpg = cv2.imencode('.jpg', frame)
        try:
            sock.sendall(jpg.tobytes() + b'END_OF_IMAGE')
        except (BrokenPipeError, ConnectionResetError):
            print("Connection lost. Reconnecting...")
            break

    sock.close()
    cap.release()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <ip_address>")
        sys.exit(1)

    ip_address = sys.argv[1]
    send_video(ip_address)
