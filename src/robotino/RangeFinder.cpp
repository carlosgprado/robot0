//
// HC-SR04 Ultrasound sensor
//

#include "Arduino.h"
#include "RangeFinder.h"

RangeFinder::RangeFinder(int trigPin, int echoPin) {
    _trigPin = trigPin;
    _echoPin = echoPin;

    // Setup
    pinMode(_trigPin, OUTPUT);
    pinMode(_echoPin, INPUT);
    digitalWrite(_trigPin, LOW);
}

float RangeFinder::getDistance() {
    // Measure the distant to an object in front
    // of the sensor (in cm.)
    
    // Emit a 10 us burst
    digitalWrite(_trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(_trigPin, LOW);

    // Read echo
    duration = pulseIn(_echoPin, HIGH);
    distance = duration / 58.2;

    return distance;
}


