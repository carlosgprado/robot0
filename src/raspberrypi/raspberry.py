# -------------------------------------------------
# Raspberry Pi component of robot0
# -------------------------------------------------

import time
import serial


def main():
    # Setup serial connection
    ser = serial.Serial(
        '/dev/ttyAMA0',     # serial dev (aliased as /dev/serial1)
        9600,               # baudrate (must match the Arduino)
        timeout=1           # timeout (1 sec.)
            )


if __name__ == '__main__':
    main()

