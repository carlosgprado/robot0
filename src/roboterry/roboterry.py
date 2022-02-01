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
g_dist = {'left': 0, 'front': 0, 'right': 0}
c = threading.Condition()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--locked", help="Lock motors by software (safe testing)", action='store_true', default=False)
    parser.add_argument("--speed", help="Initial speed (0-100)", action='store')
    args = parser.parse_args()

    motor_thread = MotorThread(locked=args.locked, speed=args.speed)
    comms_thread = CommsThread()

    print("[+] Starting threads...")

    motor_thread.start()
    comms_thread.start()

    comms_thread.join()
    motor_thread.join()

    # Cleanup
    if mc is not None:
        print("[+] robot0 stopped")
        mc.stop()


class MotorThread(threading.Thread):
    def __init__(self, name="motor", locked=False, speed=None):
        threading.Thread.__init__(self)
        self.name = name
        self.locked = locked
        self.speed = speed
        self.last_dis = [0, 0, 0]
        self.last_dis_change = time.time()

    def run(self):
        global mc

        # -------------------------------------
        # Setup motor controller
        # -------------------------------------
        if self.speed is not None:
            _speed = float(self.speed)
            mc = MotorController(initial_speed=_speed)
        else:
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
            self.track_distances()
            time.sleep(0.05)

    def track_distances(self):
        curr_dis = [
                g_dist['left'],
                g_dist['front'],
                g_dist['right']
                ]

        if curr_dis == [80, 80, 80]:
            # We are moving.
            # We have a clear line of sight
            self.last_dis_change = time.time()
            self.last_dis = curr_dis
            return

        diffs = map(
                lambda t: abs(t[0] - t[1]),
                zip(curr_dis, self.last_dis)
                )

        # The sum of all distance differences
        # in this interval of time.
        # When the robot is stuck this is very
        # small, although not null due to sensor noise
        total_displacement = sum(diffs)

        if total_displacement > 0.5:
            # We are moving
            # TODO: the threshold above is arbitrary
            #  may need tweaking...
            self.last_dis_change = time.time()
            self.last_dis = curr_dis

        # Check whether we are stuck, i.e. distances
        # not changing for a long period of time
        time_since_move = time.time() - self.last_dis_change
        if time_since_move >= 3:
            print("[-] I am stuck!")
            mc.backward(1)
            f = random.choice([mc.turn_left, mc.turn_right])
            f(1)

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
            # mc.stop()
            # mc.backward(1)

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
            # mc.stop()
            # mc.backward(1)

            # Turn left
            mc.turn_left(1)
            mc.forward()


class CommsThread(threading.Thread):
    def __init__(self, name="comms"):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global g_dist

        ld = 0
        fd = 0
        rd = 0

        # Measurements of distances larger
        # than this value are -very- noisy
        measure_max = 80  # approx (cm.)

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
            data = bytez.decode('utf-8')

            try:
                l, f, r = data.split(",")

                # Apply a cutoff
                [ld, fd, rd] = [float(x) if float(x) < measure_max else measure_max for x in (l, f, r)]
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
                'left': ld,
                'front': fd,
                'right': rd
                }


if __name__ == '__main__':
    main()

