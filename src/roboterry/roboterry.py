# -------------------------------------------------
# Raspberry Pi component of robot0
# -------------------------------------------------

import time
import random
import threading
import argparse

from helpers.serial_comms import Cereal
from helpers.motors import MotorController

# Global vars
# Thread sync is hard :)
mc = None
c = threading.Condition()





def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--locked", action='store_true', default=False)
    args = parser.parse_args()

    motor_thread = MotorThread(locked=args.locked)
    comms_thread = CommsThread()

    motor_thread.start()
    comms_thread.start()

    comms_thread.join()
    motor_thread.join()

    print("[+] Threads started")


class MotorThread(threading.Thread):
    def __init__(self, name="motor", locked=False):
        threading.Thread.__init__(self)
        self.name = name
        self.locked = locked

    def run(self):
        global mc

        # -------------------------------------
        # Setup microcontroller
        # -------------------------------------
        mc = MotorController()

        print("[+] Motor controller OK")
        print("[+]", mc)

        # Sicher is sicher
        if self.locked:
            mc.lock()

        print("[+] Motor is locked: ", mc.is_locked())

        # TODO: more movements or whatever
        print("[+] Going forward...")
        mc.forward()


class CommsThread(threading.Thread):
    def __init__(self, name="comms"):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        min_distance = 25
        adjusted_speed = 100

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
            except Exception as e:
                # Failed to convert to float
                # Probably garbage data
                print(f"[-] WAT DIS: {data}")
                mc.stop()
                continue

            print(f"[+] dis: {distance:.2f}, speed: ({mc.speed_left:.2f}, {mc.speed_right:.2f})")
            # -----------------------------------------
            # The sensor outputs some weird shit 
            # sometimes. We need some failsafes.
            # -----------------------------------------
            if distance < 0:
                # Weird shit, indeed
                # Poll more data, maybe transitory
                mc.stop()
                print(f"[-] -ENEG: {distance}")
                continue

            # -----------------------------------------
            # The sensor appears to measure max. 400 cm
            # Diminishing distances will result in 
            # lower speeds.
            # NOTE: the max. distance this can measure
            #       is around 400 cm
            # -----------------------------------------
            if distance > 100:
                adjusted_speed = 100 / 3
            else:
                adjusted_speed = distance / 3

            mc.set_speed(adjusted_speed)

            # -----------------------------------------
            # If we are too close to something, STAHP.
            # -----------------------------------------
            if distance <= min_distance:
                print(f"[+] STAHP: {distance} cm.")
                mc.stop()
                mc.backward(1)

                # Turn around
                mc.turn_right(2)

                # NOTE: when doing movements with a timeout
                #  the thread is blocked, meaning the input
                #  queue is filling up.
                #  We need to either:
                #  - flush it
                #  - pass the movement information to the 
                #    MotorController thread (better)
                cereal._reset_queues()
            else:
                mc.forward()


if __name__ == '__main__':
    main()

