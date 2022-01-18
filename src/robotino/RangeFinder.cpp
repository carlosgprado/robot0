//
// HC-SR04 Ultrasound sensor
//

#include "Arduino.h"
#include "RangeFinder.h"


/** Constructor */
RangeFinder::RangeFinder(int trigPin, int echoPin) {
    _trigPin = trigPin;
    _echoPin = echoPin;

    // Initialize the HCSR04 object
    _phc = new HCSR04(_trigPin, _echoPin);

    // Setup
    pinMode(_trigPin, OUTPUT);
    pinMode(_echoPin, INPUT);
    digitalWrite(_trigPin, LOW);
}

float RangeFinder::getDistance() {
    // Measure the distant to an object in front
    // of the sensor (in cm.)

    return _phc->dist();
}

