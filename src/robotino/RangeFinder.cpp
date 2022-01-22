//
// HC-SR04 Ultrasound sensor
//

#include "Arduino.h"
#include "RangeFinder.h"


/** Constructor (for one sensor) */
RangeFinder::RangeFinder(int trigPin, int echoPin) {
    _trigPin = trigPin;
    _echoPin = echoPin;

    // Initialize the HCSR04 object
    _phc = new HCSR04(_trigPin, _echoPin);
}

/** Constructor (for multiple sensors) */
RangeFinder::RangeFinder(int trigPin, int echoPins[], int n) {
    _trigPin = trigPin;
    _echoPins = echoPins;
    _nr_sensors = n;

    // Initialize the HCSR04 object
    _phc = new HCSR04(_trigPin, _echoPins, _nr_sensors);
}

float RangeFinder::getDistance(int n) {
    return _phc->dist(n);
}

float RangeFinder::getDistance() {
    // Measure the distant to an object in front
    // of the sensor (in cm.)

    return _phc->dist();
}

