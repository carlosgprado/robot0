# ---------------------------------------------
# Shuts down by "listening" to GPIO
#
# NOTE: add this at the end of /etc/rc.local:
#       "sudo python3 /path/to/shutdown.py &"
# ---------------------------------------------

import os
import time
import RPi.GPIO as gpio



def shutdown_pi(channel):
    print(f"[+] Shutting down! (channel: {channel})")
    time.sleep(5)
    os.system("sudo shutdown -h now")


def main():
    gpio.setmode(gpio.BCM)

    # Setup pin 21 with pullups enabled
    gpio.setup(21, gpio.IN, pull_up_down=gpio.PUD_UP)

    # Define a callback to execute when the event
    # falling edge is detected on GPIO 21
    gpio.add_event_detect(
            21, 
            gpio.FALLING, 
            callback=shutdown_pi, 
            bouncetime=2000
            )

    print("[+] Be sure to shutdown by pressing the button! ;)")

    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()

