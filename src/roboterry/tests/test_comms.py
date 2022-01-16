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
	print("[+] Reading some lines...")
	while True:
		bytez = cereal.receive_line()
		if bytez:
			data = bytez.strip(b"\r\n")
			if data:
				distance = float(data)
				print("[+] ", distance, type(distance))
				time.sleep(0.1)


if __name__ == '__main__':
	main()

