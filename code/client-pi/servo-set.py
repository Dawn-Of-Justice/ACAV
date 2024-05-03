import board
from adafruit_motor import servo as servo_module
from adafruit_pca9685 import PCA9685

def set_servo_angle(servo_number, angle):
    if servo_number < 16:
        if servo_number == 3:
           angle = 180 - angle 
        if angle > 180:
            angle = angle % 180
        i2c = board.I2C()
        pca = PCA9685(i2c)
        pca.frequency = 50
        my_servo = servo_module.Servo(pca.channels[servo_number])
        my_servo.angle = angle
        pca.deinit()
    else:
        print("Error: Servo number must be under 16")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python servo.py <servo_number> <angle>")
        sys.exit(1)
    servo_number = int(sys.argv[1])
    angle = int(sys.argv[2])
    set_servo_angle(servo_number, angle)