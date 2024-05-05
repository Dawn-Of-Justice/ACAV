import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Set up the ESC pin (change to the correct pin number)
esc_pin = 18
GPIO.setup(esc_pin, GPIO.OUT)

# Set up the PWM frequency (change to the correct frequency)
pwm_frequency = 50

# Create a PWM object
pwm = GPIO.PWM(esc_pin, pwm_frequency)

# Set the initial duty cycle (0-100%)
initial_duty_cycle = 0
pwm.start(initial_duty_cycle)

try:
    while True:
        # Get user input for the motor speed (0-100%)
        speed = int(input("Enter motor speed (0-100%): "))

        # Calculate the duty cycle based on the speed
        duty_cycle = speed / 100.0

        # Set the duty cycle
        pwm.ChangeDutyCycle(duty_cycle)

        # Wait for a short period of time
        time.sleep(0.1)

except KeyboardInterrupt:
    # Clean up
    pwm.stop()
    GPIO.cleanup()