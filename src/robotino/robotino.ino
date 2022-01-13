/**
  * Arduino component for robot0
  *
  */


void setup() {
    // Setup the serial connection
    Serial.begin(9600);

    // HC-SR04 ultrasonic module
    setup_rangefinder();
}


void loop() {
    // Wait for serial data
    // while (!Serial) {}
    // if (Serial.available() > 0) { /* do stuff with serial data */ }
    }

