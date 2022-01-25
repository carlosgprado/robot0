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
RangeFinder::RangeFinder(int trigPin, int* echoPins, int n) {
    _trigPin = trigPin;
    _echoPins = echoPins;
    _nr_sensors = n;

    // Initialize the HCSR04 object
    _phc = new HCSR04(_trigPin, _echoPins, _nr_sensors);
}

float RangeFinder::getDistance(int n) {
    float dist = _phc->dist(n);

    if (dist == 0.0) {
        // Damn it, err on the side of caution
        dist = 100.0;
    }

    return dist;
}

float RangeFinder::getDistance() {
    // Measure the distant to an object in front
    // of the sensor (in cm.)

    return getDistance(0);
}

