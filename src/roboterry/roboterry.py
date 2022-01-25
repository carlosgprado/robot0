# -------------------------------------------------
# Raspberry Pi component of robot0
# -------------------------------------------------

import time
import random
import threading
import argparse
from turtle import right

from helpers.serial_comms import Cereal
from helpers.motors import MotorController

# Global vars
# Thread sync is hard :)
mc = None
g_dist = {'left': 0, 'front': 0, 'right': 0}
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

        while True:
            self.adjust_movement()
            time.sleep(0.05)

    def adjust_movement(self):
        stop_distance = 30

        # Read this info written by the "comms" thread
        # This comes from the sensors connected at the Arduino
        left_d = g_dist['left']
        front_d = g_dist['front']
        right_d = g_dist['right']

        print(f"[+] dis: ({left_d:.2f}, {front_d:.2f}, {right_d:.2f}), speed: {mc.speed:.2f}")

        # Take an action depending on which side is closer 
        # to an obstacle

        if left_d <= stop_distance:
            print(f"[+] STAHP LEFT")
            mc.stop()
            mc.backward(1)

            # Turn right
            mc.turn_right(1)
            mc.forward()

        elif front_d <= stop_distance:
            print(f"[+] STAHP FRONT")
            mc.stop()
            mc.backward(1)

            # Chose where to turn
            if left_d < right_d:
                mc.turn_right(1)
            elif right_d < left_d:
                mc.turn_left(1)
            else:
                # The robot is equally close to left and right
                # Perform a random turn
                f = random.choice([mc.turn_left, mc.turn_right])
                f(1)

            mc.forward()

        elif right_d <= stop_distance:
            print(f"[+] STAHP RIGHT")
            mc.stop()
            mc.backward(1)

            # Turn left
            mc.turn_left(1)
            mc.forward()


class CommsThread(threading.Thread):
    def __init__(self, name="comms"):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global g_dist

        left_d = 0
        front_d = 0
        right_d = 0

        # -------------------------------------
        # Setup serial communication
        # with the Arduino
        # -------------------------------------
        try:
            cereal = Cereal(
                device_name='/dev/ttyACM0',
                baud_rate=115200,
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
            data = bytez.strip(b"\r\n")

            try:
                l, f, r = data.split(b",")
                left_d = float(l)
                front_d = float(f)
                right_d = float(r)
            except Exception as e:
                # Failed to convert to float
                # Probably garbage data
                print(f"[-] WAT DIS: {data}")

                # Stop just in case
                mc.stop()
                continue

            # We communicate this info to the Motor thread
            # by writing to this shared global variable
            g_dist = {
                'left': left_d,
                'front': front_d,
                'right': right_d
                }


if __name__ == '__main__':
    main()

