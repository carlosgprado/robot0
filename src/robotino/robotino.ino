/**
  * Arduino component for robot0
  *
  */

#include "RangeFinder.h"
#include "MiniDisplay.h"


// SSD1306 128x64 I2C
// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// HC-SR04 ultrasonic module
// trig pin = 7
// echo pin = 8
RangeFinder rf01(7, 8);


void setup() {
    // Setup the serial connection
    Serial.begin(9600);

  // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { 
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }

  // Show initial display buffer contents on the screen --
  // the library initializes this with an Adafruit splash screen.
  display.display();
  delay(2000); // Pause for 2 seconds

  // Clear the buffer
  display.clearDisplay();

  // Draw a single pixel in white
  display.drawPixel(10, 10, WHITE);

  // Show the display buffer on the screen. You MUST call display() after
  // drawing commands to make them visible on screen!
  display.display();
  delay(2000);

  display.clearDisplay();
  display.setTextSize(1);             // Normal 1:1 pixel scale
  display.setTextColor(WHITE);        // Draw white text
  display.setCursor(0,0);             // Start at top-left corner
  display.println(F("Hello, World!"));
  display.display();
}


void loop() {
    // Wait for serial data
    // while (!Serial) {}
    // if (Serial.available() > 0) { /* do stuff with serial data */ }

    Serial.println(rf01.getDistance());
    delay(60);
}

