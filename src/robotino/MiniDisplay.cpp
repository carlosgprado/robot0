//
// SSD1306 I2C Mini Display
//

#include "MiniDisplay.h"


// Constructor
MiniDisplay::MiniDisplay(int w, int h) {
    // Declaration of an SSD1306 display connected to I2C (SDA, SCL pins)
    _pd = new Adafruit_SSD1306(w, h, &Wire, OLED_RESET);

    // MOAR initialization
    height = h;
    width = w;
}

bool MiniDisplay::begin() {
    if (_pd->begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
        // SSD1306_SWITCHCAPVCC = generate display
        // voltage from 3.3V internally
        return true;
    }

    return false;
}

bool MiniDisplay::is_message_displayed() {
    unsigned long now = millis();

    if (now > msg_expires && msg_expires > 0) {
        // The expiration date for this message has passed

        if (is_scrolling) {
            // The message is scrolling. Stop it.
            no_scroll();
        }

        return false
    }

    return true;
}

void MiniDisplay::clear() {
    _pd->clearDisplay();
}

void MiniDisplay::display() {
    _pd->display();
}

void MiniDisplay::invert(bool bInvert) {
    _pd->invertDisplay(bInvert);
}

void MiniDisplay::message(const char *msg, int16_t x, int16_t y, int16_t lasts) {
    clear();

    _pd->setTextSize(1);
    _pd->setTextColor(WHITE);
    _pd->setCursor(x, y);
    _pd->println(msg);

    display();

    // Set the expiration time for this message
    msg_expires = millis() + lasts;
}

void MiniDisplay::large_message(const char *msg, int16_t x, int16_t y, int16_t lasts) {
    clear();

    _pd->setTextSize(2);
    _pd->setTextColor(WHITE);
    _pd->setCursor(x, y);
    _pd->println(msg);

    display();

    // Set the expiration time for this message
    msg_expires = millis() + lasts;
}

void MiniDisplay::warning(const char *msg, int16_t x, int16_t y, int16_t lasts) {
    clear();

    _pd->setTextSize(1);
    // Inverse text
    _pd->setTextColor(SSD1306_BLACK, SSD1306_WHITE);
    _pd->setCursor(x, y);
    _pd->println(msg);

    display();

    // Set the expiration time for this message
    msg_expires = millis() + lasts;
}

void MiniDisplay::scroll(const char *msg, int16_t x, int16_t y, int16_t lasts) {
    is_scrolling = true;
    large_message(msg, x , y);
    _pd->startscrollright(0x00, 0x0F);

    // Set the expiration time for this message
    msg_expires = millis() + lasts;
}

void MiniDisplay::no_scroll() {
    _pd->stopscroll();
    is_scrolling = false;
}

void MiniDisplay::normal_eyes() {
    // NOTE: xxxCircle(x, y, r, color)

    int16_t max_r = min(width, height) / 2;

    // Left eyeball (larger)
    _pd->drawCircle(0.30 * width, 0.40 * height, 0.75 * max_r, SSD1306_WHITE);
    _pd->fillCircle(0.35 * width, 0.42 * height, 4, SSD1306_WHITE);

    // Right eyeball (smaller)
    _pd->drawCircle(0.75 * width, 0.50 * height, 0.55 * max_r, SSD1306_WHITE);
    _pd->fillCircle(0.80 * width, 0.52 * height, 3, SSD1306_WHITE);
}

void MiniDisplay::blinking_eyes() {
    // Left blink
    _pd->drawLine(0.35 * width - 20, 0.42 * height - 10, 0.35 * width, 0.42 * height, SSD1306_WHITE);
    _pd->drawLine(0.35 * width - 16, 0.42 * height + 8, 0.35 * width, 0.42 * height, SSD1306_WHITE);

    // Right blink
    _pd->drawLine(0.80 * width, 0.52 * height, 0.80 * width + 16, 0.52 * height - 10, SSD1306_WHITE);
    _pd->drawLine(0.80 * width, 0.52 * height, 0.72 * width + 18, 0.52 * height + 0, SSD1306_WHITE);

}

void MiniDisplay::normal_mouth() {
    // Mouth
    _pd->drawLine(0.3 * width, 0.95 * height, 0.7 * width, 0.88 * height, SSD1306_WHITE);
}

void MiniDisplay::normal_face() {
    // Put a face on it!
    clear();

    normal_eyes();
    normal_mouth();

    display();
}

void MiniDisplay::blinking_face() {
    // Blinking eyez: ><
    // NOTE: drawLine(x1, y1, x2, y2, color)
    clear();

    blinking_eyes();
    normal_mouth();

    display();
}

void MiniDisplay::do_blink(int t = 200) {
    // Trick: let's make sure that the normal face 
    // is present before blinking.
    //
    // NOTE: This will BLOCK, due to the delay.
    // This is inaceptable if we are reading from
    // an ultrasound sensor for example.
    normal_face();
    delay(250);
    blinking_face();
    delay(t);
    normal_face();
}

