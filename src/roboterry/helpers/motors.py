# ----------------------------------------
# Motor(s) controller
#
# L298N Pinout
# ------------
# 
# - In1 Blue GPIO 23
# - In2 Yellow GPIO 24
# - In3 Green GPIO 22
# - In4 White GPIO 27
# ----------------------------------------

import time
import RPi.GPIO as gpio

LOW = 0
HIGH = 1


class MotorController:
    def __init__(self):
        self.right_in = 23  # In1
        self.right_out = 24 # In2
        self.left_in = 22   # In3
        self.left_out = 27  # In4
        self.left_en = 13   # EnA
        self.right_en = 12  # EnB

        self.panic_pin = 25  # Emergency stop

        # PWM
        self.left_pwm = None
        self.right_pwm = None

        gpio.setwarnings(False)

        self.locked = False
        self.speed = 33
        self.speed_left = 33
        self.speed_right = 33

        self._setup_pins()
        self._install_motor_failsafe()

        self.stop()

    def _setup_pins(self):
        gpio.setmode(gpio.BCM)

        gpio.setup(self.right_in, gpio.OUT)
        gpio.setup(self.right_out, gpio.OUT)
        gpio.setup(self.left_in, gpio.OUT)
        gpio.setup(self.left_out, gpio.OUT)
        gpio.setup(self.left_en, gpio.OUT)
        gpio.setup(self.right_en, gpio.OUT)

        # PWM
        self.left_pwm = gpio.PWM(self.left_en, 1000)
        self.right_pwm = gpio.PWM(self.right_en, 1000)

        self.left_pwm.start(self.speed_left)
        self.right_pwm.start(self.speed_right)

    def _install_motor_failsafe(self):
        """Installs a GPIO event callback.

        The Arduino will pull up a pin if it detects
        an obstacle to be too close. Generally this 
        will not need to kick in (the RPi will take
        care of it first), but better safe than broken robot
        """

        gpio.setup(
                self.panic_pin,
                gpio.IN,
                pull_up_down=gpio.PUD_UP
                )

        gpio.add_event_detect(
                self.panic_pin,
                gpio.RISING,
                callback=self._emergency_stop,
                bouncetime=500
                )

        print("[+] Installed motor fail-safe")


    def _emergency_stop(self):
        self.stop()
        print("[+] Emergency stop executed!")

    def check_lock(f):
        def wrapper(self, *args):
            if self.locked:
                print("[+] Motors are locked by software.")
            else:
                f(self, *args)

        return wrapper

    def stop(self):
        """Collaborate and listen"""

        gpio.output(self.left_in, LOW)
        gpio.output(self.left_out, LOW)
        gpio.output(self.right_in, LOW)
        gpio.output(self.right_out, LOW)

        # Stop PWM
        # self.left_pwm.stop()
        # self.right_pwm.stop()

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def is_locked(self):
        return self.locked

    # ------------------------------------------------
    # Set speed
    # ------------------------------------------------
    @check_lock
    def _set_speed_left(self, speed=0):
        """Speed between 0.0, 100.0"""

        self.speed_left = speed
        self.left_pwm.ChangeDutyCycle(speed)

    @check_lock
    def _set_speed_right(self, speed=0):
        """Speed between 0.0, 100.0"""

        self.speed_right = speed
        self.right_pwm.ChangeDutyCycle(speed)

    @check_lock
    def set_speed(self, speed=0):
        """Speed between 0.0, 100.0"""

        self.speed = speed

        self._set_speed_left(self.speed)
        self._set_speed_right(self.speed)

    # ------------------------------------------------
    # Elementary movements (independent sides)
    # ------------------------------------------------
    @check_lock
    def _left_forward(self, timeout=0):
        gpio.output(self.left_in, LOW)
        gpio.output(self.left_out, HIGH)

        if timeout > 0:
            time.sleep(timeout)
            self.stop()

    @check_lock
    def _right_forward(self, timeout=0):
        gpio.output(self.right_in, LOW)
        gpio.output(self.right_out, HIGH)

        if timeout > 0:
            time.sleep(timeout)
            self.stop()

    @check_lock
    def _left_backward(self, timeout=0):
        gpio.output(self.left_in, HIGH)
        gpio.output(self.left_out, LOW)

        if timeout > 0:
            time.sleep(timeout)
            self.stop()

    @check_lock
    def _right_backward(self, timeout=0):
        gpio.output(self.right_in, HIGH)
        gpio.output(self.right_out, LOW)

        if timeout > 0:
            time.sleep(timeout)
            self.stop()

    # ------------------------------------------------
    # Basics movements (forward, backward, etc.)
    # These are combinations of elementary movements
    # ------------------------------------------------
    @check_lock
    def forward(self, timeout=0):
        """Call without arguments to go forward forever"""

        # The combination defines the motor polarity
        # May need tweaking due to wrong cabling assumptions
        self._right_forward()
        self._left_forward()

        if timeout > 0:
            time.sleep(timeout)
            self.stop()

    @check_lock
    def backward(self, timeout=0):
        """Call without arguments to go backwards forever"""

        self._right_backward()
        self._left_backward()

        if timeout > 0:
            time.sleep(timeout)
            self.stop()

    @check_lock
    def turn_right(self, timeout=0):
        """Call without arguments to circle forever :)"""

        # The motors can not do this at low speeds.
        # Temporarily set this to 100% for the turn
        saved_speed = self.speed_left
        self._set_speed_left(100)
        self._left_forward()

        if timeout > 0:
            time.sleep(timeout)
            self.stop()

        self._set_speed_left(saved_speed)

    @check_lock
    def turn_left(self, timeout=0):
        """Call without arguments to circle forever :)"""

        # The motors can not do this at low speeds.
        # Temporarily set this to 100% for the turn
        saved_speed = self.speed_right
        self._set_speed_right(100)
        self._right_forward()

        if timeout > 0:
            time.sleep(timeout)
            self.stop()

        self._set_speed_right(saved_speed)

    @check_lock
    def turn_right_backward(self, timeout=0):
        """Call without arguments to circle forever"""

        saved_speed = self.speed_left
        self._set_speed_left(100)
        self._left_backward()

        if timeout > 0:
            time.sleep(timeout)
            self.stop()

        self._set_speed_left(saved_speed)

    @check_lock
    def turn_left_backward(self, timeout=0):
        """Call without arguments to circle forever"""

        saved_speed = self.speed_right
        self._set_speed_right(100)
        self._right_backward()

        if timeout > 0:
            time.sleep(timeout)
            self.stop()

        self._set_speed_right(saved_speed)


