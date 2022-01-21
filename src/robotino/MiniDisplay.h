#ifndef MiniDisplay_h
#define MiniDisplay_h

#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)

// Logo stuff
#define LOGO_HEIGHT   16
#define LOGO_WIDTH    16

static const unsigned char PROGMEM logo_bmp[] = {
  B00000000, B11000000,
  B00000001, B11000000,
  B00000001, B11000000,
  B00000011, B11100000,
  B11110011, B11100000,
  B11111110, B11111000,
  B01111110, B11111111,
  B00110011, B10011111,
  B00011111, B11111100,
  B00001101, B01110000,
  B00011011, B10100000,
  B00111111, B11100000,
  B00111111, B11110000,
  B01111100, B11110000,
  B01110000, B01110000,
  B00000000, B00110000 
};


class MiniDisplay {
    public:
        int height = 0;
        int width = 0;

        // Constructor
        MiniDisplay(int w, int h);

        // Methods
        bool begin();
        void clear();
        void display();
        void invert(bool bInvert);

        // Text stuff
        void message(const char *msg, int16_t x = 0, int16_t y = 0);
        void large_message(const char *msg, int16_t x = 0, int16_t y = 0);
        void warning(const char *msg, int16_t x = 0, int16_t y = 0);
        void scroll(const char *msg, int16_t x = 0, int16_t y = 0);
        void no_scroll();

        // Face stuff :)
        void normal_face();
        void blink_face();
        void do_blink(int t = 200);
    private:
        Adafruit_SSD1306 *_pd;
};

#endif

