# -------------------------------------------------
# Raspberry Pi component of robot0
# -------------------------------------------------

import time
from helpers.serial_comms import Cereal
from helpers.motors import MotorController


def main():
    # -------------------------------------
    # Setup serial communication
    # with the Arduino
    # -------------------------------------
    try:
        cereal = Cereal(
            device_name='/dev/ttyACM0',
            baud_rate=9600,
            timeout=1
            )
    except Exception as e:
        print(e)
        return 1

    # -------------------------------------
    # Setup MotorController
    # -------------------------------------
    mc = MotorController()

    # Sicher ist sicher
    mc.lock()


if __name__ == '__main__':
    main()

