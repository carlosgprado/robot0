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

void MiniDisplay::clear() {
    _pd->clearDisplay();
}

void MiniDisplay::display() {
    _pd->display();
}

void MiniDisplay::print_message(const char *msg) {
    clear()
    _pd->setTextSize(1);
    _pd->setTextColor(WHITE);
    _pd->setCursor(0, 0);
    _pd->println(msg);
    display();
}

void MiniDisplay::show_face() {
    // Put a face on it!
    clear();
    int16_t radius = max(width, height) / 2;

    // x, y, r, color
    _pd->fillCircle(width / 2, height / 2, radius, SSD1306_WHITE);
    display();
}


