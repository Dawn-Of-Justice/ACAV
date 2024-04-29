import time
import board
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

def set_servo_angle(angle):
    global servo
    i2c = board.I2C()
    pca = PCA9685(i2c)
    pca.frequency = 50
    servo = servo.Servo(pca.channels[0])
    servo.angle = angle

    fraction = 0.0
    while fraction < 1.0:
        servo.fraction = fraction
        fraction += 0.01
        time.sleep(0.03)

    pca.deinit()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python servo.py <angle>")
        sys.exit(1)
    angle = int(sys.argv[1])
    set_servo_angle(angle)