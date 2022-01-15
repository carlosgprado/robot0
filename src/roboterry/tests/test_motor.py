import time
import sys
sys.path.append(r"/home/pi/c0de/robot0/src/roboterry")

from helpers.motors import MotorController

mc = None


def main():
	global mc

	mc = MotorController()

	# back_and_forth(times=3)
	mc.backward(4)

	forward_and_right_turn(times=3)


def back_and_forth(times=1):
	for _ in range(times):
		mc.backward(1.5)
		mc.forward(1.5)

def forward_and_right_turn(times=1):
	for _ in range(times):
		mc.forward(0.8)
		time.sleep(0.5)
		mc.turn_right(0.8)


if __name__ == '__main__':
	main()

