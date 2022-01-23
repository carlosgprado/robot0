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
// echo pin left = 8
// echo pin center = 9
// echo pin right = 10
RangeFinder rf(7, new int[3]{8, 9, 10}, 3);


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

    if (md01.is_message_displayed) {
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

void send_range_info() {
    // --------------------------------------------------
    // Read from the range sensors and send the data
    // to the Raspberry Pi for motion processing
    // --------------------------------------------------
    char buf[24] = {0};
    char left[6] = {0};
    char front[6] = {0};
    char right[6] = {0};

    // Convert the float values to char*    
    dtostrf(rf.getDistance(0), 4, 2, left);
    dtostrf(rf.getDistance(1), 4, 2, front);
    dtostrf(rf.getDistance(2), 4, 2, right);

    strcpy(buf, left);
    strcat(buf, ",");
    strcpy(buf, front);
    strcat(buf, ",");
    strcpy(buf, right);

    md01.message(buf);
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
    char buf[512];

    // Serial.println(rf.getDistance());
    delay(60);

    send_range_info();

    // -----------------------------------------
    // "Face management" :)
    // Keep this always at the end
    // -----------------------------------------
    // track_the_blinks();
}

