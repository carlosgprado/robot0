# -------------------------------------------------
# Raspberry Pi component of robot0
# -------------------------------------------------

import time
from helpers.serial_comms import Cereal


def main():
    cereal = Cereal(
        device_name='/dev/ttyAMA0',
        baud_rate=9600,
        timeout=1
        )


if __name__ == '__main__':
    main()

