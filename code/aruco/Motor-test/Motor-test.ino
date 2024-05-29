#include <Servo.h>

#define MIN_PULSE_LENGTH 1000 // Minimum pulse length in µs
#define MAX_PULSE_LENGTH 2000 // Maximum pulse length in µs

#define SETUP_MIN_PULSE_LENGTH 1000
#define SETUP_MAX_PULSE_LENGTH 1050

Servo motA;
Servo motB;
const int controlPin = 2; // Pin to control the motor
bool motorRunning = false;

void setup() {
    Serial.begin(9600);

    motA.attach(3, SETUP_MIN_PULSE_LENGTH, SETUP_MAX_PULSE_LENGTH);
    motB.attach(5, SETUP_MIN_PULSE_LENGTH, SETUP_MAX_PULSE_LENGTH);

    motA.writeMicroseconds(1000);
    motB.writeMicroseconds(1000);

    pinMode(controlPin, INPUT);

    displayInstructions();
}

void loop() {
    int controlState = digitalRead(controlPin);
    static int lastControlState = LOW;

    if (controlState == HIGH && lastControlState == LOW) {
        if (!motorRunning) {
            startMotor(1050); // Start motor from 1000 to 1500
            motorRunning = true;
        }
    } else if (controlState == LOW && lastControlState == HIGH) {
        if (motorRunning) {
            stopMotor(); // Stop motor
            motorRunning = false;
        }
    }

    lastControlState = controlState;
}

void startMotor(int targetSpeed) {
    for (int i = MIN_PULSE_LENGTH; i <= targetSpeed; i += 5) {
        Serial.print("Pulse length = ");
        Serial.println(i);

        motA.writeMicroseconds(i);
        motB.writeMicroseconds(i);

        delay(20);
    }
    Serial.println("Motor started at speed");
}

void stopMotor() {
    for (int i = motA.readMicroseconds(); i >= MIN_PULSE_LENGTH; i -= 5) {
        Serial.print("Pulse length = ");
        Serial.println(i);

        motA.writeMicroseconds(i);
        motB.writeMicroseconds(i);

        delay(20);
    }
    Serial.println("Motor stopped");
}

void displayInstructions()
{  
    Serial.println("READY - PLEASE SEND INSTRUCTIONS AS FOLLOWING :");
    Serial.println("\tControl pin is connected to pin 2");
}