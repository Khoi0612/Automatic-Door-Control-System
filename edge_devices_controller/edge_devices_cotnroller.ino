#include <Servo.h>

const int trigPin = 3;
const int echoPin = 4;
const int ldrPin = A0;
const int ledPin = 8;
const int servoPin = 9;

bool doorOpened = false;
bool alarmOn = false;

bool manualControl = false;  // Tracks if actuators can be trontrolled manually

Servo doorServo;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledPin, OUTPUT);
  doorServo.attach(servoPin);
  doorServo.write(0);  // Door closed
}

void loop() {
  // Distance calculation
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW); 
  long duration = pulseIn(echoPin, HIGH);
  float distance = duration * 0.034 / 2;
  bool personDetected = (distance < 50);

  // Light level calculation
  int lightLevel = analogRead(ldrPin);
  bool isBright = lightLevel > 400;

  // Check for serial commands
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "manual") {
      manualControl = !manualControl;  // Activate manual override
    }

    if (command == "door") {
      if (manualControl) {
        doorOpened = !doorOpened;  // Toggle door state
      }
    }

    if (command == "alarm") {
      if (manualControl) {
        alarmOn = !alarmOn;  // Toggle alarm state
      }
    }
  }

  // ---Door Control---
  if (!manualControl) {
    // Only apply automatic control if not in manual override
    if (personDetected && isBright) {
      // At day when there are people
      doorOpened = true;
    } else {
      // At night or no people
      doorOpened = false;
    }
  }

  // ---Alarm Control---
  if (!manualControl) {
    // Only apply automatic control if not in manual override
    if (personDetected && !isBright) {
      // At night when there are people
      alarmOn = true;
    } else {
      alarmOn = false;
    }
  }

  // Apply physical controls
  doorServo.write(doorOpened ? 90 : 0);
  digitalWrite(ledPin, alarmOn ? HIGH : LOW);

  // Serial output to edge server
  Serial.print("Distance:");
  Serial.print(distance);
  Serial.print(", Light:");
  Serial.print(lightLevel);
  Serial.print(", Manual Control:");
  Serial.print(manualControl ? "Manual" : "Auto");
  Serial.print(", Door:");
  Serial.print(doorOpened ? "Open" : "Closed");
  Serial.print(", Alarm:");
  Serial.println(alarmOn ? "On" : "Off");

  delay(500);  // Check every half a second
}