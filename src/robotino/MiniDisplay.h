#ifndef MiniDisplay_h
#define MiniDisplay_h

#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)


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
        void message(const char *msg, bool c = true, int16_t x = 0, int16_t y = 0);
        void large_message(const char *msg, int16_t x = 0, int16_t y = 0);
        void warning(const char *msg, int16_t x = 0, int16_t y = 0);
        void scroll(const char *msg, int16_t x = 0, int16_t y = 0);
        void no_scroll();

        // Face stuff :)
        void normal_eyes();
        void normal_mouth();
        void blinking_eyes();

        void normal_face();
        void blinking_face();
        void do_blink(int t = 200);
    private:
        Adafruit_SSD1306 *_pd;
};

#endif

