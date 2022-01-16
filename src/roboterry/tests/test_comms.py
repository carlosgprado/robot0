import time
import sys
sys.path.append(r"/home/pi/c0de/robot0/src/roboterry")

from helpers.serial_comms import Cereal


def main():
	try:
		# Try the default values
		cereal = Cereal()
	except Exception as e:
		print(e)
		return 1

	print("[+] Serial comms seem fine :)")
	print(cereal)

	# Read some lines and print to screen
	print("[+] Readins some lines...")
	for _ in range(10):
		bytez = cereal.receive_line()
		if bytez:
			print("[+] ", bytez)
		else:
			print("[-] Input buffer is empty")


if __name__ == '__main__':
	main()

