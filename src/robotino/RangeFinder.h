#ifndef RangeFinder_h
#define RangeFinder_h

#include "Arduino.h"

class RangeFinder {
    public:
        int duration = 0;
        int distance = 0;

        // Constructor
        RangeFinder(int trigPin, int echoPin);

        // Methods
        float getDistance();

    private:
        int _trigPin;
        int _echoPin;
};

#endif

