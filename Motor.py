

import board
from adafruit_pca9685 import PCA9685

# # Create the I2C bus interface.
i2c = board.I2C()  # uses board.SCL and board.SDA
# # i2c = busio.I2C(board.GP1, board.GP0)    # Pi Pico RP2040

# # Create a simple PCA9685 class instance.
pca = PCA9685(i2c)

# # Set the PWM frequency to 60hz.
pca.frequency = 60

# Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
# but the PCA9685 will only actually give 12 bits of resolution.

value = 20

duty_cycle = (value / 100.0) * 65535
# print(duty_cycle)
print(hex(int(duty_cycle)))

pca.channels[0].duty_cycle = hex(int(duty_cycle))



class Motion:

    def __init__(self,*args):

        self.pca = pca

        self.fservo = self.pca.channels[args[0]]
        self.bservo = self.pca.channels[args[1]]

        self.head_servo = self.pca.channels[args[2]]

        self.wheels = self.pca.channels[args[3]]

    def move_wheels(self, dutycycle=0x7FFF):
        self.wheels.duty_cycle = duty_cycle

    def stop_wheels(self, duty_cycle = 0):
        self.wheels.duty_cycle = duty_cycle

    def head(self, angle):

        self.head_servo.angle = angle

    def front_servo(self, angle):
        self.fservo.angle = angle

    def rear_servo(self, angle):
            self.bservo.angle = angle
