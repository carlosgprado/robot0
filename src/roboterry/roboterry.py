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
        max_distance = 200
        min_distance = 30

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

            print("[+] Serial comms OK")
            print("[+]", cereal)
        except Exception as e:
            print(e)
            return 1

        while True:
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

                # Update the maximum distance
                if distance > max_distance:
                    max_distance = distance
            except Exception as e:
                # Failed to convert to float
                # Probably garbage data
                print(f"[-] WAT DIS: {data}")
                continue

            print(distance)
            # -----------------------------------------
            # The sensor appears to measure max. 111 cm
            # Diminishing distances will result in 
            # lower speeds
            # -----------------------------------------
            delta = distance - min_distance
            gamma = max_distance - min_distance

            adjusted_speed = ((delta + 0.0) / gamma) * 100
            # Just in case :)
            if adjusted_speed > 100:
                adjusted_speed = 100

            if adjusted_speed < 0:
                # This can happen due to spurious values
                # in the input buffer (e.g. 0.0)
                adjusted_speed = 33

            mc.set_speed(adjusted_speed)

            # -----------------------------------------
            # If we are too close to something, STAHP.
            # -----------------------------------------
            if distance <= min_distance:
                print(f"[+] STAHP: {distance} cm.")
                mc.stop()
                mc.backward()
            else:
                mc.forward()


if __name__ == '__main__':
    main()

