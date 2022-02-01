import time
import sys
sys.path.append(r"/home/pi/c0de/robot0/src/roboterry")

from helpers.motors import MotorController

mc = None


def main():
    global mc

    mc = MotorController()

    back_and_forth(times=2)

    # Test locking mechanism
    mc.lock()

    # Should abort with an error message
    mc.forward(1)

    # Unlock the motors
    mc.unlock()

    # This will work, since we are unlocked
    mc.turn_left(1.5)
    mc.turn_right_backward(1.5)
    mc.turn_right(1.5)
    mc.turn_left_backward(1.5)


def loop_circle(times=1):
	for _ in range(times):
		mc.turn_left(timeout=4)
		mc.turn_right(timeout=4)


def back_and_forth(times=1):
	for _ in range(times):
		mc.backward(1.5)
		mc.forward(1.5)


def forward_and_right_turn(times=1):
	for _ in range(times):
		mc.forward(0.5)
		time.sleep(0.2)
		mc.turn_right(0.5)


if __name__ == '__main__':
	main()

