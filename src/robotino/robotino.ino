/**
  * Arduino component for robot0
  *
  */

#include "RangeFinder.h"
#include "MiniDisplay.h"

#define SSD1306_NO_SPLASH


bool is_message_displayed = false;

// SSD1306 128x64 I2C
MiniDisplay md01(SCREEN_WIDTH, SCREEN_HEIGHT);

// HC-SR04 ultrasonic module
// trig pin = 7
// echo pin = 8
RangeFinder rf01(7, 8);


void splash() {
    // ------------------------
    // Dynamic splash message
    // ------------------------
    md01.large_message("robot0", 30, 25);

    for(uint8_t i = 0; i <= 3; i++) {
        md01.invert(true);
        delay(250);
        md01.invert(false);
        delay(250);
    }

    // Blink a couple of times :)
    for (uint8_t i=0; i < 2; i++) {
        md01.do_blink();
        delay(2000);
    }

}

void track_the_blinks() {
    // --------------------------------------
    // This keeps some state to keep track
    // of the face's blinking state
    // --------------------------------------
    static unsigned long last_blink = 0;
    static bool is_blink_face = false;

    if (is_message_displayed) {
        // An important message is on screen
        // Skip these face shenanigans
        return;
        }

    if (is_blink_face) {
        if (millis() - last_blink > 200) {
            md01.normal_face();
            is_blink_face = false;
            }
        }

    if (millis() - last_blink > 2000) {
        last_blink = millis();  // TOCTOU, LOL
        is_blink_face = true;
        md01.blinking_face();
        }
}

void setup() {
    // Setup the serial connection
    Serial.begin(9600);

    // Setup the MiniDisplay
    if(!md01.begin()) { 
      Serial.println(F("SSD1306 allocation failed"));
      for(;;); // Don't proceed, loop forever
    }

    // Be classy
    splash();
}


void loop() {
    // Wait for serial data
    // while (!Serial) {}
    // if (Serial.available() > 0) { /* do stuff with serial data */ }

    // Serial.println(rf01.getDistance());
    delay(60);

    // test display
    if (millis() > 20000 && millis() < 25000) {
        md01.large_message("IMPORTANT SHIT");
        is_message_displayed = true;
    }

    if (millis() > 25000)
        is_message_displayed = false;

    Serial.println(millis());

    // "Face management" :)
    // Keep this always at the end
    track_the_blinks();
}
