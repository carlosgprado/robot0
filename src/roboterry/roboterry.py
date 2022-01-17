# -------------------------------------------------
# Raspberry Pi component of robot0
# -------------------------------------------------

import time
import random
import threading

from helpers.serial_comms import Cereal
from helpers.motors import MotorController

# Global vars
# Thread sync is hard :)
mc = None
c = threading.Condition()


def main():
    
    motor_thread = MotorThread()
    comms_thread = CommsThread()

    motor_thread.start()
    comms_thread.start()

    comms_thread.join()
    motor_thread.join()

    print("[+] Threads started")


class MotorThread(threading.Thread):
    def __init__(self, name="motor"):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global mc

        # -------------------------------------
        # Setup microcontroller
        # -------------------------------------
        mc = MotorController()

        print("[+] Motor controller OK")
        print("[+]", mc)

        # Sicher is sicher
        # mc.lock()

        print("[+] Motor is locked: ", mc.is_locked())

        time.sleep(1)

        # TODO: more movements or whatever
        mc.forward()
        print("[+] Going forward...")


class CommsThread(threading.Thread):
    def __init__(self, name="comms"):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        # -------------------------------------
        # Setup serial communication
        # with the Arduino
        # -------------------------------------
        try:
            cereal = Cereal(
                device_name='/dev/ttyACM0',
                baud_rate=57600,
                timeout=1
                )

            print("[+] Serial comms OK")
            print("[+]", cereal)
        except Exception as e:
            print(e)
            return 1

        while True:
            # time.sleep(0.005)
            bytez = cereal.receive_line()

            if not bytez:
                continue

            # There is data on the input buffer
            # TODO: right now the data is only distance
            #  but it may be necessary to process this
            #  input latter (maybe CSV?)

            data = bytez.strip(b"\r\n")
            try:
                distance = float(data)
            except Exception as e:
                # Failed to convert to float
                # Probably garbage data
                continue

            print(distance)
            # -----------------------------------------
            # If we are too close to something, STAHP.
            # -----------------------------------------
            if distance <= 30:
                print(f"[+] STAHP: {distance} cm.")
                mc.stop()


if __name__ == '__main__':
    main()

