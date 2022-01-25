/**
  * Arduino component for robot0
  *
  */

#include "RangeFinder.h"
#include "MiniDisplay.h"

#define SSD1306_NO_SPLASH
#define PANIC_PIN 6


// SSD1306 128x64 I2C
MiniDisplay md01(SCREEN_WIDTH, SCREEN_HEIGHT);

// HC-SR04 ultrasonic modules
int trig_left = 2;
int echo_left = 3;
int trig_front = 4;
int echo_front = 5;
int trig_right = 7;
int echo_right = 8;

RangeFinder rf_left(trig_left, echo_left);
RangeFinder rf_front(trig_front, echo_front);
RangeFinder rf_right(trig_right, echo_right);


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

    if (md01.is_message_displayed()) {
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
    float dangerous_d = 20.0;
    float min_d = 0.0;
    float left_d = 0.0;
    float front_d = 0.0;
    float right_d = 0.0;

    left_d = rf_left.getDistance();
    front_d = rf_front.getDistance();
    right_d = rf_right.getDistance();

    // oooooo Emergency break oooooo
    // Find the minimum distance
    if (left_d < front_d && left_d < right_d)
        min_d = left_d;
    else if (front_d < right_d)
        min_d = front_d;
    else
        min_d = right_d;

    if (min_d <= dangerous_d && min_d > 0) {
        // Pump the brakes!
        digitalWrite(PANIC_PIN, HIGH);
        md01.large_message("TOO CLOSE!", 0, 0, 1500);
    }

    Serial.print(left_d);
    Serial.print(",");
    Serial.print(front_d);
    Serial.print(",");
    Serial.println(right_d);

    delay(200);

    // Reset the panic pin
    digitalWrite(PANIC_PIN, LOW);
}

void setup() {
    // Setup the serial connection
    Serial.begin(115200);

    // Initialize the panic pin (emergency break)
    pinMode(PANIC_PIN, OUTPUT);
    digitalWrite(PANIC_PIN, LOW);

    // Setup the MiniDisplay
    if(!md01.begin()) { 
      Serial.println(F("SSD1306 allocation failed"));
      for(;;); // Don't proceed, loop forever
    }

    // Be classy
    splash();
}


void loop() {
    send_range_info();

    // -----------------------------------------
    // "Face management" :)
    // Keep this always at the end
    // -----------------------------------------
    track_the_blinks();
}

