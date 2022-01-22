#ifndef RangeFinder_h
#define RangeFinder_h

#include "Arduino.h"
#include <HCSR04.h>

class RangeFinder {
    public:
        int duration = 0;
        int distance = 0;

        // Constructors
        RangeFinder(int trigPin, int echoPin);
        RangeFinder(int trigPin, int* echoPins, int n);

        // Methods
        float getDistance();
        float getDistance(int n);

    private:
        int _trigPin;
        int _echoPin;
        int _nr_sensors;

        HCSR04* _phc;

        int* _echoPins;
};

#endif

