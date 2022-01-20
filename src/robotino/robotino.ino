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

    md01.message("Hola, Kieran!");
    delay(1000);
    md01.large_message("robot0");
    md01.invert(true);
    delay(2000);
    md01.invert(false);
    delay(500);

    // Blink
    for (int i=0; i < 3; i++) {
        md01.do_blink(200);
        delay(2000);
    }

    md01.message("Normal message");
    delay(1000);

    md01.large_message("Large message");
    delay(1000);

    md01.warning("Nostromo will autodestruct in 10 mins");
    delay(1000);

    md01.scroll("YUUUGGEE");
    delay(1000);
    md01.no_scroll();   
}


void loop() {
    // Wait for serial data
    // while (!Serial) {}
    // if (Serial.available() > 0) { /* do stuff with serial data */ }

    Serial.println(rf01.getDistance());
    delay(60);

    md01.message(String(millis()).c_str());
}

