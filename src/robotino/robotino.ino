/**
  * Arduino component for robot0
  *
  */

#include "RangeFinder.h"
#include "MiniDisplay.h"

#define SSD1306_NO_SPLASH


// SSD1306 128x64 I2C
MiniDisplay md01(SCREEN_WIDTH, SCREEN_HEIGHT);

// HC-SR04 ultrasonic module
// trig pin = 7
// echo pin = 8
RangeFinder rf01(7, 8);


void setup() {
    // Setup the serial connection
    Serial.begin(9600);

    if(!md01.begin()) { 
      Serial.println(F("SSD1306 allocation failed"));
      for(;;); // Don't proceed, loop forever
    }

    md01.print_message("Hola, Kieran!");
    delay(1000);
    md01.normal_face();
    md01.invert(true);
    delay(2000);
    md01.invert(false);
    delay(500);
    for (int i=0; i <= 5; i++) {
        md01.do_blink(200);
        delay(1000);
    }
}


void loop() {
    // Wait for serial data
    // while (!Serial) {}
    // if (Serial.available() > 0) { /* do stuff with serial data */ }

    Serial.println(rf01.getDistance());
    delay(60);
}

